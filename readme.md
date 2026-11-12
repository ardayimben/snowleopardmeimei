# Snow Leopard Meimei – Pew Pew Pew

A fun desktop toy made of little bouncing windows that move to the beat of a song. Close a window and it splits in two, the music speeds up, and the screen slowly fills with more and more windows.

Project: https://github.com/ardayimben/snowleopardmeimei

## How it works

1. When the program starts, the song begins playing.
2. At specific moments in the song (`SPAWN_TIMES`), image windows drop onto the screen and bounce off the floor.
3. If you close a window with the X button, it doesn't just disappear: it stretches sideways, shakes, and splits into two smaller windows.
4. Every split makes the song a little faster (its pitch rises too).
5. Windows also multiply on their own over time. There is an upper limit so your computer doesn't freeze (`MAX_WINDOWS`).
6. When the song ends, it restarts and everything begins again.

Windows squash when they hit the ground and stretch as they launch. The higher they fall from, the higher they bounce.

## Installation

Requires Python 3.8+.

```bash
git clone https://github.com/ardayimben/snowleopardmeimei.git
cd snowleopardmeimei
pip install pygame pillow numpy
```

`tkinter` ships with Python. If it's missing on Linux, install it separately (`sudo apt install python3-tk`).

## Files

Put these two files in the **same folder** as `anne.py`:

| File | Purpose |
|---|---|
| `Pew Pew Pew.mp3` | The song |
| `meimei.webp` | The image shown in the windows |

Different file names are fine too: the program first looks for these exact names, and if it can't find them, it uses any `.mp3` and `.webp` file in the same folder. It also checks your Downloads folder.

## Running

```bash
python anne.py
```

**To quit**, press `ESC` in any window. You can also finish by closing all the windows one by one.

## Settings

All settings are at the top of `anne.py`. Some of them:

| Setting | Description |
|---|---|
| `SPAWN_TIMES` | At which seconds of the song windows appear |
| `IMAGE_WIDTH` | Window width (px) |
| `SPEED_STEP` / `SPEED_MAX` | Speed increase per split and the upper limit |
| `SPEED_DECAY_SECONDS` | If set, speed resets after this many seconds (`None` = off) |
| `GRAVITY` | Gravity strength |
| `CLONE_INTERVAL` / `CLONE_CHANCE` | How often and how likely windows multiply on their own |
| `MAX_WINDOWS` | Maximum number of windows at once |
| `STRETCH_PX` | How far a window stretches before splitting |

## Troubleshooting

- **"X is not installed" error:** Install the missing package with `pip install`.
- **"File not found" error:** Make sure the `.mp3` and `.webp` files are in the same folder as `anne.py`.
- **Audio not supported error:** Only 16-bit audio output is supported.
- **Computer slows down:** Lower `MAX_WINDOWS`.

## Built with

- [pygame](https://www.pygame.org/) – audio
- [Pillow](https://python-pillow.org/) – image processing
- [NumPy](https://numpy.org/) – speeding up the song (resampling)
- `tkinter` – windows
