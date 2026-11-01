# Mei Mei Desktop Companion

An interactive desktop application built in Python that creates dynamic screen animations and audio effects featuring Mei Mei the cat and her Snow Leopard form.

The app manages floating desktop windows using Tkinter, handles realtime image scaling with Pillow, and uses Pygame's lower-level audio buffer features to synchronize sound pitch and speed with window behavior.

## Features

* Window Animations: Spawns and bounces floating desktop windows containing custom images across the screen.
* Visual Splitting: Windows stretch, shake, and split into multiple smaller windows (representing Snow Leopard Mei Mei's multiplication).
* Real-time Audio Processing: Audio buffer manipulation dynamically adjusts song playback speed and pitch based on app events.
* Simple Controls: Close active windows or press the Escape key on an open window to exit.

## Prerequisites

* Python 3.8 or higher
* Pillow
* pygame

## Setup and Running

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mei-mei-desktop.git
   cd mei-mei-desktop
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the media file paths near the top of `anne.py` to point to your local assets:
   ```python
   muz = r"C:\path\to\your\audio.mp3"
   kedi = r"C:\path\to\meimei_image.webp"
   ```

4. Run the application:
   ```bash
   python anne.py
   ```

## Built With

* Standard Library: `tkinter`, `array`, `fractions`, `time`, `random`, `os`, `sys`
* Pillow (PIL): Image loading, resizing, and Tkinter canvas rendering
* Pygame: Raw audio buffer manipulation and sound playback