import copy
import ctypes
from threading import Thread, Lock
from time import time, sleep

import cv2
import img as img
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from mss import mss

from util.jsonfunction import getJson, applyJsonConfig
from util.pixel import getImgRectangle

user32 = ctypes.WinDLL('user32', use_last_error=True)

gameName = ""


def find_window(hwnd, strings):
    global gameName
    window_title = win32gui.GetWindowText(hwnd)
    #print(window_title)
    if gameName in window_title:
        print(window_title)
        strings.append(hwnd)


class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    w_diff = 0
    h_diff = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    stopped = True
    lock = None
    screenshot = None
    modifiedScreenshot = None

    def __init__(self, game_name, fps=False, imgGrab=False):
        global gameName
        gameName = game_name
        applyJsonConfig(self, "window")
        self.imgGrab = imgGrab
        if self.imgGrab:
            self.sct = mss()
        winList = []
        win32gui.EnumWindows(find_window, winList)
        print(winList)
        if len(winList) > 0:
            self.hwnd = winList[0]
        else:
            self.hwnd = win32gui.FindWindow(None, game_name)

        self.activate()
        self.x, self.y, self.x1, self.y1 = win32gui.GetWindowRect(self.hwnd)

        self.fps = fps
        self.lock = Lock()
        self.h = self.y1 - self.y + self.h_diff
        self.w = self.x1 - self.x + self.w_diff
        print(self.x, self.y, self.w, self.h)
        self.offset_x = self.x + self.cropped_x
        self.offset_y = self.y + self.cropped_y
        self.center = {"x": round(self.w / 2), "y": round(self.h / 2)}
        self.halfSize = (int(self.w / 2), int(self.h / 2))

    def copy(self):
        return copy.deepcopy(self.screenshot)

    def activate(self):
        win32gui.SetForegroundWindow(self.hwnd)

    def coorAsList(self):
        return {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}

    def stop(self):
        self.stopped = True

    def getScreenshot(self, region=None):
        if not self.imgGrab:
            screenshot = self.getBaseScreenShot()
        else:
            screenshot = self.getImgGrab()
        return screenshot if region is None else getImgRectangle(screenshot,region)

    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y

    def getImgGrab(self):
        return np.array(self.sct.grab(self.coorAsList()))[..., :3]

    def getBaseScreenShot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDc = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDc.SelectObject(dataBitMap)
        cDc.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        signedIntArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dcObj.DeleteDC()
        cDc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img
