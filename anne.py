import os
import sys
import time
import random
import tkinter as tk
from array import array
from fractions import Fraction
from tkinter import messagebox

try:
    from PIL import Image as gorsel, ImageTk as gorseltk
except ImportError:
    gorsel = gorseltk = None

pizza = tk.Tk()
pizza.withdraw()

sucuk = pizza.winfo_screenwidth()
elma = pizza.winfo_screenheight()

muz = r"C:\Users\user\Downloads\Pew Pew Pew.mp3"
kedi = r"C:\Users\user\Downloads\4624ea3b60d5d3b628619261f38ea5fb.webp"
cay = [3.6, 5.5, 7.5, 9.0, 11.0]
simit = 0.0

ekmek = 340
peynir = 0.35
zeytin = 16

domates = 0.1
biber = 3.0
patates = False
sogan = 2.5

balik = 0.45
kus, at = 15, 19

araba = 150
bisiklet = 70
ucak = 30

kopek, kurt = 17, 21
ordek, tavuk = 11, 16
inek, koyun = 1.5, 3.0
ceviz = 0.8
fistik = 140

kebap = 10
lahmacun = 0.2

masa, sandalye = 340, 200
kapi = elma - sandalye - 80
perde = None
hali = None
limon = None
portakal = None

bardak = 0
tabak = len(cay)
kasik = None
sepet = []


def catal(fark):
    global bardak
    bardak += fark
    if bardak <= 0 and tabak <= 0:
        pizza.after(300, lambda: pizza.destroy()
                    if bardak <= 0 and tabak <= 0 else None)


def bicak():
    if kasik is not None:
        kasik.eldiven()


def tencere(kirmizi, mavi, yesil, sari):
    kova = tk.Toplevel(pizza)
    kova.title(" ")
    kova.attributes("-topmost", True)
    kova.configure(bg="black")
    kova.geometry(f"{kirmizi}x{mavi}{yesil:+d}{sari:+d}")
    kova.bind("<Escape>", lambda e: pizza.destroy())
    return kova


def tava(kutu, cerceve):
    salata = tk.Label(kutu, image=cerceve, bd=0, highlightthickness=0,
                      padx=0, pady=0, bg="black")
    salata.pack(fill="both", expand=True)
    return salata


def kazan(t):
    return 1 - (1 - t) ** 3


class Kavun:
    def __init__(self, oyun, ses):
        self.bir = oyun
        self.iki, uc, self.dort = oyun.mixer.get_init()
        if uc != -16:
            raise RuntimeError("Desteklenmeyen ses formatı (16-bit bekleniyordu).")
        self.bes = 2 * self.dort

        self.alti = ses.get_raw()
        self.yedi = len(self.alti) / (self.iki * self.bes)
        sekiz = array("h")
        sekiz.frombytes(self.alti)
        dokuz = len(sekiz) // self.dort
        sekiz = sekiz[:dokuz * self.dort]
        self.on = [sekiz[c::self.dort] for c in range(self.dort)]

        self.kalem = 0.0
        self.silgi = 0
        self.defter = Fraction(1)
        self.kitap = 1.0
        self.canta = time.perf_counter()
        self.okul = 0.0
        self.sinif = None
        self.tahta = None

    def ayakkabi(self, nane):
        hamur, un = self.defter.numerator, self.defter.denominator
        yumurta = [c[nane:] for c in self.on]
        su = len(yumurta[0])
        tuz = (su * un) // hamur
        if tuz < 100:
            return b""
        seker = array("h", bytes(2 * tuz * self.dort))
        for sut, bal in enumerate(yumurta):
            yag = array("h", bytes(2 * tuz))
            for tereyag in range(un):
                recel = len(range(tereyag, tuz, un))
                yag[tereyag::un] = bal[(tereyag * hamur) // un::hamur][:recel]
            seker[sut::self.dort] = yag
        return seker.tobytes()

    def corap(self):
        if self.sinif is not None:
            self.sinif.stop()
        nane = int(self.kalem * self.iki)
        if self.defter == 1:
            limonata = self.alti[nane * self.bes:]
        else:
            limonata = self.ayakkabi(nane)
        if len(limonata) < self.bes * 100:
            self.sinif = None
            return
        self.tahta = self.bir.mixer.Sound(buffer=limonata)
        self.sinif = self.tahta.play()

    def gomlek(self):
        kola = min(1.0 + self.silgi * domates, biber)
        soda = Fraction(kola).limit_denominator(20)
        if soda == self.defter:
            return
        self.defter = soda
        self.kitap = float(soda)
        self.corap()
        self.canta = time.perf_counter()

    def pantolon(self):
        self.kalem = 0.0
        self.corap()
        self.canta = time.perf_counter()

    def ceket(self):
        return self.kalem >= self.yedi

    def sapka(self):
        self.silgi = 0
        self.defter = Fraction(1)
        self.kitap = 1.0
        self.okul = 0.0
        self.kalem = 0.0
        self.corap()
        self.canta = time.perf_counter()

    def atki(self):
        ayran = time.perf_counter()
        self.kalem += (ayran - self.canta) * self.kitap
        self.canta = ayran
        if patates and self.silgi > 0 and ayran >= self.okul:
            self.silgi = 0
            self.gomlek()

    def eldiven(self):
        self.atki()
        self.silgi += 1
        self.okul = time.perf_counter() + sogan
        self.gomlek()
        print(f"Şarkı hızı: {self.kitap:.2f}x")


class Karpuz:
    def __init__(self, sira):
        self.canli = True
        self.tavsan = random.randint(0, max(0, sucuk - masa))
        self.aslan = random.randint(0, max(1, kapi // 2))
        self.fil = 0.0
        self.zebra = sucuk / 2 - masa / 2 + (sira - 2) * (masa + 10)
        self.zebra = max(0, min(self.zebra, sucuk - masa))
        self.kaplan = random.uniform(0.6, 1.2)

        self.ayi = tencere(masa, sandalye, int(self.tavsan), int(self.aslan))
        self.panda = tava(self.ayi, hali)
        sepet.append(self)
        self.ayi.protocol("WM_DELETE_WINDOW", self.maymun)
        catal(+1)
        self.yilan()

    def yilan(self):
        if not self.canli:
            return
        self.fil += balik
        self.aslan += self.fil
        if self.aslan >= kapi:
            self.aslan = kapi
            self.fil = -random.uniform(kus, at)

        if abs(self.tavsan - self.zebra) > self.kaplan:
            self.tavsan += self.kaplan if self.tavsan < self.zebra else -self.kaplan

        self.ayi.geometry(f"{masa}x{sandalye}{int(self.tavsan):+d}{int(self.aslan):+d}")
        self.ayi.after(zeytin, self.yilan)

    def maymun(self):
        self.canli = False
        if self in sepet:
            sepet.remove(self)
        cx, cy = int(self.tavsan), int(self.aslan)
        self.ayi.destroy()
        Armut(perde, cx, cy)
        catal(-1)

    def cogal(self):
        Kiraz(perde, int(self.tavsan), int(self.aslan),
              yon=random.choice((-1, 1)))


class Armut:
    def __init__(self, bulut, eylul, ekim):
        self.bulut = bulut
        self.yildiz, self.gunes = bulut.size
        self.ay = araba * self.yildiz / masa
        self.dag = elma - self.gunes - 80
        self.deniz = eylul
        self.aslan = max(0, min(ekim, self.dag))
        self.nehir = 0
        self.gol = False
        self.orman, self.col = eylul, eylul + self.yildiz
        self.tepe = bulut

        self.ayi = tencere(self.yildiz, self.gunes, eylul, self.aslan)
        self.vadi = gorseltk.PhotoImage(self.tepe)
        self.panda = tava(self.ayi, self.vadi)
        self.ayi.protocol("WM_DELETE_WINDOW", self.sonuc)
        catal(+1)
        self.yilan()

    def yilan(self):
        if self.gol:
            return
        self.nehir += 1

        if self.nehir <= bisiklet:
            saat = self.nehir / bisiklet
            yagmur = self.ay * kazan(saat)
            self.orman = max(0, int(self.deniz - yagmur))
            self.col = min(sucuk, int(self.deniz + self.yildiz + yagmur))
            kar = self.col - self.orman
            self.tepe = self.bulut.resize((kar, self.gunes), limon)
            self.vadi = gorseltk.PhotoImage(self.tepe)
            self.panda.config(image=self.vadi)
            self.ayi.geometry(f"{kar}x{self.gunes}{self.orman:+d}{self.aslan:+d}")
        else:
            ruzgar = self.nehir - bisiklet
            if ruzgar > ucak:
                self.makas()
                return
            firtina = 1 + 5 * ruzgar / ucak
            sis = int(random.uniform(-firtina, firtina))
            dolu = int(random.uniform(-firtina, firtina))
            self.ayi.geometry(
                f"{self.col - self.orman}x{self.gunes}"
                f"{self.orman + sis:+d}{max(0, self.aslan + dolu):+d}")

        self.ayi.after(zeytin, self.yilan)

    def makas(self):
        self.gol = True
        ocak = (self.orman + self.col) // 2
        subat = self.aslan
        mart = max(fistik, int(self.yildiz * ceviz))
        nisan = max(1, int(self.gunes * mart / self.yildiz))
        self.ayi.destroy()
        bicak()
        mayis = self.bulut.resize((mart, nisan), portakal)
        haziran = max(0, ocak - mart)
        temmuz = min(sucuk - mart, ocak)
        Kiraz(mayis, haziran, subat, yon=-1)
        Kiraz(mayis, temmuz, subat, yon=+1)
        catal(-1)

    def sonuc(self):
        if self.gol:
            return
        self.gol = True
        self.ayi.destroy()
        catal(-1)


class Kiraz:
    def __init__(self, tepe, eylul, ekim, yon):
        self.tepe = tepe
        self.arpa, self.bugday = tepe.size
        self.dag = elma - self.bugday - 80
        self.tavsan = float(eylul)
        self.aslan = float(ekim)
        self.yon = yon
        self.kaplan = random.uniform(inek, koyun)
        self.fil = -random.uniform(kopek, kurt)
        self.gol = False

        self.ayi = tencere(self.arpa, self.bugday, int(self.tavsan), int(self.aslan))
        self.vadi = gorseltk.PhotoImage(tepe)
        self.panda = tava(self.ayi, self.vadi)
        sepet.append(self)
        self.ayi.protocol("WM_DELETE_WINDOW", self.maymun)
        catal(+1)
        self.yilan()

    def yilan(self):
        if self.gol:
            return

        self.fil += balik
        self.aslan += self.fil
        self.tavsan += self.yon * self.kaplan

        if self.aslan >= self.dag:
            self.aslan = self.dag
            self.fil = -random.uniform(ordek, tavuk)

        if self.aslan < 0:
            self.aslan = 0
            self.fil = abs(self.fil) * 0.5

        if self.tavsan < 0:
            self.tavsan = 0
            self.yon = 1
        elif self.tavsan + self.arpa > sucuk:
            self.tavsan = sucuk - self.arpa
            self.yon = -1

        self.ayi.geometry(f"{self.arpa}x{self.bugday}{int(self.tavsan):+d}{int(self.aslan):+d}")
        self.ayi.after(zeytin, self.yilan)

    def maymun(self):
        if self.gol:
            return
        self.gol = True
        if self in sepet:
            sepet.remove(self)
        ax, ay = int(self.tavsan), int(self.aslan)
        tepe = self.tepe
        self.ayi.destroy()
        Armut(tepe, ax, ay)
        catal(-1)

    def cogal(self):
        Kiraz(self.tepe, int(self.tavsan), int(self.aslan),
              yon=random.choice((-1, 1)))


def fincan(yazi):
    messagebox.showerror("Hata", yazi, parent=pizza)
    pizza.destroy()
    sys.exit(1)


def cezve(sira):
    global tabak
    tabak -= 1
    Karpuz(sira)


def kumar():
    for kurban in list(sepet):
        if random.random() < lahmacun:
            kurban.cogal()
    pizza.after(int(kebap * 1000), kumar)


def semaver():
    global kasik, masa, sandalye, kapi, perde, hali, limon, portakal

    if not os.path.isfile(muz):
        fincan(f"Ses dosyası bulunamadı:\n{muz}\n\n"
               "Dosyanın yolunu kodun başındaki muz değişkenine yaz.")

    if not os.path.isfile(kedi):
        fincan(f"Fotoğraf bulunamadı:\n{kedi}\n\n"
               "Dosyanın yolunu kodun başındaki kedi değişkenine yaz.")

    if gorsel is None:
        fincan("Pillow yüklü değil.\n\nKomut satırına şunu yaz:\n"
               "pip install pillow")

    try:
        import pygame
    except ImportError:
        fincan("pygame yüklü değil.\n\nKomut satırına şunu yaz:\n"
               "pip install pygame")

    print("Dosyalar yükleniyor...")

    try:
        corba = getattr(gorsel, "Resampling", gorsel)
        limon = corba.BILINEAR
        portakal = corba.LANCZOS
        makarna = gorsel.open(kedi).convert("RGB")
        pilav = ekmek / makarna.width
        if makarna.height * pilav > elma * peynir:
            pilav = elma * peynir / makarna.height
        masa = max(1, int(makarna.width * pilav))
        sandalye = max(1, int(makarna.height * pilav))
        perde = makarna.resize((masa, sandalye), portakal)
        hali = gorseltk.PhotoImage(perde)
        kapi = elma - sandalye - 80
    except Exception as hata:
        fincan(f"Fotoğraf yüklenemedi:\n{hata}")

    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        ses = pygame.mixer.Sound(muz)
        kasik = Kavun(pygame, ses)
    except Exception as hata:
        fincan(f"Ses yüklenemedi:\n{hata}")
    print(f"Fotoğraf ({masa}x{sandalye}) ve ses ({ses.get_length():.1f} sn) yüklendi. Başlıyor!")

    kasik.pantolon()
    pizza.after(int(kebap * 1000), kumar)
    siradaki = 0

    def dongu():
        global tabak
        nonlocal siradaki
        kasik.atki()
        if kasik.ceket():
            kasik.sapka()
            siradaki = 0
            tabak = len(cay)
            print("Şarkı bitti, hız sıfırlandı, baştan başlıyor!")
        zaman = kasik.kalem + simit
        while siradaki < len(cay) and zaman >= cay[siradaki]:
            cezve(siradaki)
            siradaki += 1
        pizza.after(5, dongu)

    dongu()


pizza.after(100, semaver)
pizza.mainloop()
