# Arda Mavi
import os
import sys
import platform
import numpy as np
from time import sleep
from PIL import ImageGrab
from PIL import Image
from game_control import *
from predict import predict
import skimage.transform as st
from game_control import get_id
from get_dataset import save_img
from multiprocessing import Process
from keras.models import model_from_json
from pynput.mouse import Listener as mouse_listener
from pynput.keyboard import Listener as key_listener, Key
import cv2
from windowcapture import WindowCapture
wc = WindowCapture("ArcheAge")

def get_screenshot():
    global wc
    img = wc.getScreenshot()

    return img

def save_event_keyboard(data_path, event, key):

    try:
        key = get_id(key.char)
    except:
        try:
            key = get_id(key)
        except:
            if key == Key.right:
                key = get_id("q")
            elif key == Key.left:
                key = get_id("d")
            elif key == Key.up:
                key = get_id("z")
            elif key == key.down:
                key = get_id("s")
            else:
                return
    data_path = data_path + '/-1,-1,{0},{1}'.format(event, key)
    screenshot = get_screenshot()
    save_img(screenshot, data_path)
    return

def save_event_mouse(data_path, x, y):

    data_path = data_path + '/{0},{1},0,0'.format(x, y)
    screenshot = get_screenshot()
    save_img(screenshot, data_path)
    return

def listen_mouse():
    data_path = 'Data/Train_Data/Mouse'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_click(x, y, button, pressed):
        save_event_mouse(data_path, x, y)

    def on_scroll(x, y, dx, dy):
        pass
    
    def on_move(x, y):
        pass

    with mouse_listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def listen_keyboard():
    data_path = 'Data/Train_Data/Keyboard'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_press(key):
        save_event_keyboard(data_path, 1, key)

    def on_release(key):
        save_event_keyboard(data_path, 2, key)

    with key_listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    dataset_path = 'Data/Train_Data/'

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # Start to listening mouse with new process:
    Process(target=listen_mouse, args=()).start()
    listen_keyboard()
    return

if __name__ == '__main__':
    main()
