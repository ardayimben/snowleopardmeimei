Mei Mei Desktop Companion

An interactive desktop application built in Python that creates dynamic screen animations and audio effects featuring Mei Mei the cat and her Snow Leopard form.

The app manages floating desktop windows using Tkinter, handles realtime image scaling with Pillow, and uses Pygame's lower-level audio buffer features to synchronize sound pitch and speed with window behavior.

Features

Window Animations: Spawns and bounces floating desktop windows containing custom images across the screen.

Visual Splitting: Windows stretch, shake, and split into multiple smaller windows (representing Snow Leopard Mei Mei's multiplication).

Real-time Audio Processing: Audio buffer manipulation dynamically adjusts song playback speed and pitch based on app events.

Simple Controls: Close active windows or press the Escape key on any open window to exit.

Variable Name Glossary

Sorry for the confusing variable names! Here is a guide to what they actually do in anne.py:

Configuration & Media

muz: Path to the .mp3 audio file.

kedi: Path to the Mei Mei image file (.webp, .png, etc.).

cay: Time stamps (in seconds) that trigger window spawning events.

simit: Time offset used during audio timing calculations.

Screen & Geometry Constants

pizza: The hidden root Tkinter instance.

sucuk / elma: Screen width and height.

ekmek, peynir, zeytin: Base dimensions, screen scaling ratios, and animation refresh rates (ms).

domates, biber, patates, sogan: Speed adjustment steps, maximum speed cap, reset flags, and speed duration timeouts.

araba, bisiklet, ucak: Animation thresholds for window stretching, shaking, and splitting transitions.

balik, kus, at: Gravity constant, bounce upward force minimum, and bounce upward force maximum.

kopek, kurt, ordek, tavuk: Horizontal and vertical bounce physics parameters for split windows.

inek, koyun, ceviz, fistik: Horizontal drift ranges, image scaling minimums, and resize constraints.

kebap, lahmacun: Timer interval for window multiplication checks and probability rate for window duplication.

masa, sandalye, kapi: Base window width, base window height, and floor collision boundary on screen.

perde, hali, limon, portakal: Resized PIL Image instance, PhotoImage object, and resampling filters.

bardak, tabak, kasik, sepet: Active window counter, remaining spawn queue count, Kavun (audio controller) instance, and list of active window objects.

Classes & Functions

catal(): Increments/decrements active window counts and terminates the main app when all windows are closed.

bicak(): Triggers audio speed acceleration when a window splits.

tencere(): Helper function to create top-level Tkinter windows (Toplevel).

tava(): Helper function to create image labels inside windows.

kazan(): Cubic easing out calculation for window animation transitions.

Kavun: Class handling audio buffering, pitch/speed manipulation, and Pygame sound playback.

Karpuz: Main bouncing window class (Mei Mei).

Armut: Stretching/shaking transition window class.

Kiraz: Split sub-window class (Snow Leopard Mei Mei units).

fincan(): Utility function displaying error message dialogs.

cezve(): Spawns a new main window from the spawn queue.

kumar(): Periodic function that handles random window duplication.

semaver(): Main setup function initializing media resources, audio buffers, and main event loops.

Prerequisites

Python 3.8 or higher

Pillow

pygame

Setup and Running

Clone this repository:

git clone https://github.com/ardayimben/snowleopardmeimei.git
cd snowleopardmeimei


Install dependencies:

pip install -r requirements.txt


Update the media file paths near the top of anne.py to point to your local assets:

muz = r"C:\path\to\your\audio.mp3"
kedi = r"C:\path\to\meimei_image.webp"


Run the application:

python anne.py


Built With

Standard Library: tkinter, array, fractions, time, random, os, sys

Pillow (PIL): Image loading, resizing, and Tkinter canvas rendering

Pygame: Raw audio buffer manipulation and sound playback
