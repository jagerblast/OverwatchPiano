import sounddevice as sd
import numpy as np
import pyautogui as inp
import ctypes
import time

MOUSEEVENTF_MOVE = 0x0001

device_id = 1

current_key = None

mouse_speed_x = 25
mouse_speed_y = 25

def set_movement(key):
    global current_key

    if key == current_key:
        return

    if current_key is not None:
        inp.keyUp(current_key)

    current_key = key

    if current_key is not None:
        inp.keyDown(current_key)

def audio_callback(indata, frames, time, status):
    audio = indata[:, 0]

    if np.abs(audio).mean() > 0.03:
        frequencies = np.fft.rfftfreq(len(audio),1/44100)
        spectrum = np.abs(np.fft.rfft(audio))

        strongest_frequency = frequencies[np.argmax(spectrum)]

        if strongest_frequency <= 70:
            set_movement(None)
            return
        elif 1319.9 < strongest_frequency <= 1400:
            inp.click()
        elif 1219 <= strongest_frequency <= 1319.9:
            inp.rightClick()
        elif 1164 <= strongest_frequency < 1219:
            set_movement("w")
        elif 1009 <= strongest_frequency < 1164:
            set_movement("a")
        elif 931 <= strongest_frequency < 1009:
            set_movement("s")
        elif 815 <= strongest_frequency < 931:
            set_movement("d")
        elif 737 <= strongest_frequency < 815:
            inp.press("space")
        elif 698.8 <= strongest_frequency < 737:
            inp.press("e")
        elif 600 <= strongest_frequency < 698.8:
            # up
            ctypes.windll.user32.mouse_event(
                MOUSEEVENTF_MOVE,
                0,
                -mouse_speed_y,
                0,
                0
                )
        elif 550 <= strongest_frequency < 600:
            # down
            ctypes.windll.user32.mouse_event(
                MOUSEEVENTF_MOVE,
                0,
                mouse_speed_y,
                0,
                0
                )
        elif 500 <= strongest_frequency < 550:
            # left
            ctypes.windll.user32.mouse_event(
                MOUSEEVENTF_MOVE,
                -mouse_speed_x,
                0,
                0,
                0
                )
        elif 427 <= strongest_frequency < 500:
            # right
            ctypes.windll.user32.mouse_event(
                MOUSEEVENTF_MOVE,
                mouse_speed_x,
                0,
                0,
                0
                )
        elif 174 <= strongest_frequency < 388:
            inp.press("shift")
        elif 70 < strongest_frequency < 174:
            inp.press("q")


        print(f"Strongest Frequency: {strongest_frequency:.1f} Hz")

with sd.InputStream(
    device=device_id,
    channels = 1,
    samplerate = 44100,
    callback=audio_callback
    ):
    print("Listening to input")
    while True:
        sd.sleep(1000)