import ctypes
import math
import random
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

try:
    import numpy as np
except ImportError:
    np = None
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

BASE_DIR = Path(__file__).resolve().parent


def find_file(name, pattern):
    for folder in (BASE_DIR, Path.home() / "Downloads"):
        candidate = folder / name
        if candidate.is_file():
            return candidate
    found = sorted(BASE_DIR.glob(pattern))
    if found:
        return found[0]
    return BASE_DIR / name


MUSIC_PATH = find_file("Pew Pew Pew.mp3", "*.mp3")
IMAGE_PATH = find_file("meimei.webp", "*.webp")

SPAWN_TIMES = [3.6, 5.5, 7.5, 9.0, 11.0]
START_OFFSET = 0.0

IMAGE_WIDTH = 340
MAX_HEIGHT_RATIO = 0.35
TASKBAR_MARGIN = 80

SPEED_STEP = 0.1
SPEED_MAX = 3.0
SPEED_DECAY_SECONDS = None

GRAVITY = 0.45
FRAME_MS = 16
POLL_MS = 8
MAX_CATCHUP = 4

RESTITUTION_LOW = 0.94
INTRO_MIN_BOUNCE = 15
HALF_MIN_BOUNCE = 11

DRIFT_MIN = 1.2
DRIFT_MAX = 4.5

SQUASH_FRAMES = 10
SQUASH_MIN_DEPTH = 0.20
SQUASH_MAX_DEPTH = 0.55
SQUASH_SPEED_DIV = 50
LAUNCH_FRAMES = 10
LAUNCH_STRETCH = 0.18
SCALE_STEPS = 50

CLONE_INTERVAL = 10
CLONE_CHANCE = 0.2
MAX_WINDOWS = 30

SPLIT_WIDTH_RATIO = 0.8
SPLIT_MIN_WIDTH = 140
STRETCH_FRAMES = 70
SHAKE_FRAMES = 30
STRETCH_PX = 150

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


def ease_out(t):
    return 1 - (1 - t) ** 3


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class SpeedPlayer:
    def __init__(self, mixer, sound):
        self.mixer = mixer
        self.rate, fmt, self.channels = mixer.get_init()
        if fmt != -16:
            raise RuntimeError("Only 16-bit audio is supported.")
        raw = np.frombuffer(sound.get_raw(), dtype=np.int16)
        raw = raw[: len(raw) // self.channels * self.channels]
        self.samples = raw.reshape(-1, self.channels)
        self.total = len(self.samples)
        self.duration = self.total / self.rate
        self.hits = 0
        self.speed = 1.0
        self.position = 0.0
        self.decay_at = 0.0
        self.last = time.perf_counter()
        self.channel = None
        self.sound = None

    def _play(self):
        if self.channel is not None:
            self.channel.stop()
        start = int(self.position * self.rate)
        if self.total - start < 100:
            self.channel = None
            return
        if self.speed == 1.0:
            chunk = self.samples[start:]
        else:
            n = int((self.total - start) / self.speed)
            pos = start + np.arange(n, dtype=np.float64) * self.speed
            i0 = pos.astype(np.int64)
            frac = (pos - i0).astype(np.float32)[:, None]
            i1 = np.minimum(i0 + 1, self.total - 1)
            chunk = (self.samples[i0] * (1 - frac) + self.samples[i1] * frac)
            chunk = chunk.astype(np.int16)
        self.sound = self.mixer.Sound(buffer=np.ascontiguousarray(chunk).tobytes())
        self.channel = self.sound.play()
        self.last = time.perf_counter()

    def _set_speed(self):
        new = min(1.0 + self.hits * SPEED_STEP, SPEED_MAX)
        if abs(new - self.speed) < 1e-6:
            return
        self.speed = new
        self._play()

    def start(self):
        self.position = 0.0
        self._play()

    def update(self):
        now = time.perf_counter()
        self.position += (now - self.last) * self.speed
        self.last = now
        if SPEED_DECAY_SECONDS and self.hits > 0 and now >= self.decay_at:
            self.hits = 0
            self._set_speed()

    def hit(self):
        self.update()
        self.hits += 1
        self.decay_at = time.perf_counter() + (SPEED_DECAY_SECONDS or 0)
        self._set_speed()
        print(f"Song speed: {self.speed:.2f}x")

    def finished(self):
        return self.position >= self.duration

    def restart(self):
        self.hits = 0
        self.speed = 1.0
        self.start()

    def stop(self):
        if self.channel is not None:
            self.channel.stop()


class Sprite:
    def __init__(self, image, resample):
        self.image = image
        self.resample = resample
        self.w, self.h = image.size
        self.cache = {}

    def photo(self, w, h, cache=True):
        key = (w, h)
        photo = self.cache.get(key)
        if photo is None:
            img = self.image if key == (self.w, self.h) \
                else self.image.resize(key, self.resample)
            photo = ImageTk.PhotoImage(img)
            if cache:
                self.cache[key] = photo
        return photo


class FloatWindow:
    can_clone = False
    cache_frames = True

    def __init__(self, app, sprite, x, y):
        self.app = app
        self.sprite = sprite
        self.w, self.h = sprite.w, sprite.h
        self.x, self.y = float(x), float(y)
        self.alive = True
        self.floor = app.screen_h - self.h - TASKBAR_MARGIN
        self.max_bounce = math.sqrt(2 * GRAVITY * max(self.floor, 1)) * 0.95

        self.sx = self.sy = 1.0
        self.phase, self.phase_t = "air", 0
        self.vy = self.next_vy = self.depth = 0.0
        self.launch_amp = LAUNCH_STRETCH
        self.dir = random.choice((-1, 1))
        self.vx = random.uniform(1.5, 3.0)
        self.drifting = False
        self.shown = (self.w, self.h)
        self.last_geo = None

        self.top = tk.Toplevel(app.root)
        self.top.title(" ")
        self.top.attributes("-topmost", True)
        self.top.configure(bg="black")
        self.top.bind("<Escape>", lambda e: app.quit())
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        self.photo = sprite.photo(self.w, self.h)
        self.label = tk.Label(self.top, image=self.photo, bd=0,
                              highlightthickness=0, bg="black")
        self.label.pack(fill="both", expand=True)
        app.windows.add(self)
        self.render()

    def size(self):
        qx = round(self.sx * SCALE_STEPS) / SCALE_STEPS
        qy = round(self.sy * SCALE_STEPS) / SCALE_STEPS
        return max(1, int(self.w * qx)), max(1, int(self.h * qy))

    def pos(self, w, h):
        return self.x + (self.w - w) / 2, self.y + self.h - h

    def render(self):
        if not self.alive:
            return
        w, h = self.size()
        if (w, h) != self.shown:
            self.photo = self.sprite.photo(w, h, cache=self.cache_frames)
            self.label.config(image=self.photo)
            self.shown = (w, h)
        x, y = self.pos(w, h)
        geo = (w, h, int(x), int(y))
        if geo != self.last_geo:
            self.last_geo = geo
            self.top.geometry(f"{w}x{h}{geo[2]:+d}{geo[3]:+d}")

    def step(self):
        pass

    def ballistic(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y < 0:
            self.y, self.vy = 0, abs(self.vy) * 0.5

    def drift_x(self):
        self.x += self.dir * self.vx
        if self.x < 0:
            self.x, self.dir = 0, 1
        elif self.x + self.w > self.app.screen_w:
            self.x, self.dir = self.app.screen_w - self.w, -1

    def land(self, impact_vy, min_bounce):
        rebound = impact_vy * random.uniform(RESTITUTION_LOW, 1.0)
        rebound = clamp(rebound, min_bounce, self.max_bounce)
        self.y = self.floor
        self.vy = 0.0
        self.next_vy = -rebound
        self.depth = clamp(impact_vy / SQUASH_SPEED_DIV,
                           SQUASH_MIN_DEPTH, SQUASH_MAX_DEPTH)
        self.launch_amp = LAUNCH_STRETCH * min(1.6, rebound / 16)
        self.phase, self.phase_t = "squash", 0
        self.drifting = True
        self.vx = clamp(self.vx + random.uniform(-0.6, 0.9), DRIFT_MIN, DRIFT_MAX)
        if random.random() < 0.2:
            self.dir = -self.dir

    def bounce_phase(self):
        if self.phase == "squash":
            self.phase_t += 1
            t = self.phase_t / SQUASH_FRAMES
            if t < 1:
                sy = 1 - self.depth * math.sin(math.pi * t / 2)
                self.sx, self.sy = 1 / math.sqrt(sy), sy
                return True
            self.phase, self.phase_t = "launch", 0
            self.vy = self.next_vy
        if self.phase == "launch":
            self.phase_t += 1
            k = 1 - self.phase_t / LAUNCH_FRAMES
            if k > 0:
                sy = 1 + self.launch_amp * k
                self.sx, self.sy = 1 / math.sqrt(sy), sy
            else:
                self.phase = "air"
                self.sx = self.sy = 1.0
        return False

    def destroy(self):
        if not self.alive:
            return
        self.alive = False
        self.app.windows.discard(self)
        self.top.destroy()
        self.app.check_done()

    def on_close(self):
        Stretch(self.app, self.sprite, self.x, self.y)
        self.destroy()

    def clone(self):
        Half(self.app, self.sprite, self.x, self.y, random.choice((-1, 1)))


class Intro(FloatWindow):
    can_clone = True

    def __init__(self, app, index):
        sprite = app.base_sprite
        super().__init__(app, sprite,
                         random.randint(0, max(0, app.screen_w - sprite.w)),
                         random.randint(0, max(1, app.screen_h // 4)))
        target = app.screen_w / 2 - sprite.w / 2 + (index - 2) * (sprite.w + 10)
        self.target_x = clamp(target, 0, app.screen_w - sprite.w)
        self.glide = random.uniform(0.6, 1.2)

    def step(self):
        if self.bounce_phase():
            return
        self.ballistic()
        if self.drifting:
            self.drift_x()
        elif abs(self.x - self.target_x) > self.glide:
            self.x += self.glide if self.x < self.target_x else -self.glide
        if self.y >= self.floor:
            self.land(self.vy, INTRO_MIN_BOUNCE)


class Half(FloatWindow):
    can_clone = True

    def __init__(self, app, sprite, x, y, direction):
        super().__init__(app, sprite, x, y)
        self.dir = direction
        self.vx = random.uniform(1.5, 3.0)
        self.vy = -random.uniform(17, 21)
        self.drifting = True

    def step(self):
        if self.bounce_phase():
            return
        self.ballistic()
        self.drift_x()
        if self.y >= self.floor:
            self.land(self.vy, HALF_MIN_BOUNCE)


class Stretch(FloatWindow):
    cache_frames = False

    def __init__(self, app, sprite, x, y):
        self.cur_w = sprite.w
        self.cx0 = int(x)
        self.cur_x = float(x)
        self.cur_y = float(y)
        self.frame = 0
        super().__init__(app, sprite, x, y)
        self.y = clamp(self.y, 0, self.floor)
        self.cur_y = self.y
        self.render()

    def size(self):
        return self.cur_w, self.h

    def pos(self, w, h):
        return self.cur_x, self.cur_y

    def on_close(self):
        self.destroy()

    def step(self):
        self.frame += 1
        if self.frame <= STRETCH_FRAMES:
            grow = STRETCH_PX * self.w / IMAGE_WIDTH * ease_out(self.frame / STRETCH_FRAMES)
            self.cx0 = max(0, int(self.x - grow))
            cx1 = min(self.app.screen_w, int(self.x + self.w + grow))
            self.cur_w = max(self.w, (cx1 - self.cx0) // 4 * 4)
            self.cur_x = float(self.cx0)
        else:
            k = self.frame - STRETCH_FRAMES
            if k > SHAKE_FRAMES:
                self.split()
                return
            amp = 1 + 5 * k / SHAKE_FRAMES
            self.cur_x = self.cx0 + random.uniform(-amp, amp)
            self.cur_y = max(0, self.y + random.uniform(-amp, amp))

    def split(self):
        mid = self.cx0 + self.cur_w // 2
        y = self.y
        w = max(SPLIT_MIN_WIDTH, int(self.w * SPLIT_WIDTH_RATIO))
        h = max(1, int(self.h * w / self.w))
        half = Sprite(self.sprite.image.resize((w, h), self.app.good), self.app.fast)
        Half(self.app, half, max(0, mid - w), y, -1)
        Half(self.app, half, min(self.app.screen_w - w, mid), y, +1)
        self.app.player.hit()
        self.destroy()


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.windows = set()
        self.next_spawn = 0
        self.closing = False
        self.quitting = False
        self.load_assets()
        self.player.start()
        self.acc = 0.0
        self.prev = time.perf_counter()
        self.root.after(CLONE_INTERVAL * 1000, self.clone_tick)
        self.loop()

    def fail(self, msg):
        messagebox.showerror("Error", msg, parent=self.root)
        self.root.destroy()
        sys.exit(1)

    def load_assets(self):
        if Image is None:
            self.fail("Pillow is not installed.\n\npip install pillow")
        if np is None:
            self.fail("numpy is not installed.\n\npip install numpy")
        try:
            import pygame
        except ImportError:
            self.fail("pygame is not installed.\n\npip install pygame")
        for path, name in ((MUSIC_PATH, "MUSIC_PATH"), (IMAGE_PATH, "IMAGE_PATH")):
            if not path.is_file():
                self.fail(f"File not found:\n{path}\n\nUpdate {name} at the top of the file.")

        res = getattr(Image, "Resampling", Image)
        self.fast, self.good = res.BILINEAR, res.LANCZOS
        try:
            img = Image.open(IMAGE_PATH).convert("RGB")
            scale = IMAGE_WIDTH / img.width
            if img.height * scale > self.screen_h * MAX_HEIGHT_RATIO:
                scale = self.screen_h * MAX_HEIGHT_RATIO / img.height
            img = img.resize((max(1, int(img.width * scale)),
                              max(1, int(img.height * scale))), self.good)
            self.base_sprite = Sprite(img, self.fast)
        except Exception as e:
            self.fail(f"Failed to load image:\n{e}")
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            sound = pygame.mixer.Sound(str(MUSIC_PATH))
            self.player = SpeedPlayer(pygame.mixer, sound)
        except Exception as e:
            self.fail(f"Failed to load audio:\n{e}")
        print(f"Image {img.size} and audio ({sound.get_length():.1f} s) loaded.")

    def loop(self):
        if self.quitting:
            return
        now = time.perf_counter()
        self.acc += (now - self.prev) * 1000
        self.prev = now
        steps = int(self.acc // FRAME_MS)
        self.acc -= steps * FRAME_MS
        steps = min(steps, MAX_CATCHUP)

        self.player.update()
        if self.player.finished():
            self.player.restart()
            self.next_spawn = 0
            print("Song finished, restarting!")
        t = self.player.position + START_OFFSET
        while self.next_spawn < len(SPAWN_TIMES) and t >= SPAWN_TIMES[self.next_spawn]:
            Intro(self, self.next_spawn)
            self.next_spawn += 1

        for _ in range(steps):
            for w in list(self.windows):
                if w.alive:
                    w.step()
        for w in list(self.windows):
            w.render()
        self.root.after(POLL_MS, self.loop)

    def clone_tick(self):
        if self.quitting:
            return
        for w in list(self.windows):
            n = len(self.windows)
            if n >= MAX_WINDOWS:
                break
            if w.can_clone and random.random() < CLONE_CHANCE * (1 - n / MAX_WINDOWS):
                w.clone()
        self.root.after(CLONE_INTERVAL * 1000, self.clone_tick)

    def check_done(self):
        pending = len(SPAWN_TIMES) - self.next_spawn
        if not self.windows and pending <= 0 and not self.closing:
            self.closing = True
            self.root.after(300, self.quit)

    def quit(self):
        if self.quitting:
            return
        self.quitting = True
        try:
            self.player.stop()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
