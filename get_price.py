import itertools
import os
from multiprocessing import Pool, Manager

import numpy as np
import pandas as pd
import pyautogui
import tesserocr
from PIL import ImageGrab, Image
from pynput import keyboard
from thefuzz import fuzz


def reduce_noise(img):
    img = np.array(img)
    height, width = img.shape[0], img.shape[1]
    img = img.tolist()

    for (x, y) in itertools.product(range(height), range(width)):
        if 90 < img[x][y][1] < 170 and 90 < img[x][y][2] < 160 and np.std(img[x][y]) > 30:
            img[x][y] = [0, 0, 0]
        else:
            img[x][y] = [255, 255, 255]
    img = np.array(img, dtype=np.dtype("uint8"))
    img = Image.fromarray(img)
    return img


def price_check(printing_lock):
    box_margin_x, box_margin_y = 400, 80
    cursor_x, cursor_y = pyautogui.position()
    img = ImageGrab.grab((cursor_x - box_margin_x, cursor_y - box_margin_y, cursor_x + box_margin_x, cursor_y + box_margin_y))
    img = reduce_noise(img)
    prices = pd.read_csv("./prices.csv").to_dict(orient="records")
    text = tesserocr.image_to_text(img, path="./Tesseract/tessdata").lower().replace("'", "")
    gems_on_screen = [gem for gem in prices if fuzz.partial_ratio(gem["name"], text) > 95]

    for gem in gems_on_screen:
        with printing_lock:
            print(f"{gem['name']} -----> {gem['chaos_value']} chaos")


def clear():
    with printing_lock:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n") # TODO: FIX ME


if __name__ == '__main__':
    os.environ["OMP_THREAD_LIMIT"] = "1"

    canonical = keyboard.Listener().canonical
    ctrl_pressed = False
    process_pool = Pool(6)
    manager = Manager()
    printing_lock = manager.Lock()
    price_check_count = 0

    with keyboard.Events() as events:
        for event in events:
            if canonical(event.key) == keyboard.Key.ctrl:
                if isinstance(event, keyboard.Events.Press):
                    ctrl_pressed = True
                if isinstance(event, keyboard.Events.Release):
                    ctrl_pressed = False
            if ctrl_pressed and canonical(event.key) == keyboard.KeyCode.from_char("a") and isinstance(event, keyboard.Events.Press):
                price_check_count += 1
                if price_check_count > 5:
                    price_check_count = 1
                    clear()
                process_pool.apply_async(price_check, args=(printing_lock,))
            if ctrl_pressed and canonical(event.key) == keyboard.KeyCode.from_char("m") and isinstance(event, keyboard.Events.Press):
                with printing_lock:
                    print("exiting...")
                break

    manager.shutdown()
    process_pool.close()
    process_pool.join()
