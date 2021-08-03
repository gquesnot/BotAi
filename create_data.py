import json

import numpy as np
import cv2
import time
import os

from util import hswfilter
from util.getkeys import key_check
from util.hswfilter import HsvFilter
from util.vision import Vision
from windowcapture import WindowCapture

file_name = "data/training_data.npy"
file_name2 = "data/target_data.npy"


class KeyData:
    k = None
    tInit = 0
    i = []
    def __init__(self):
        pass

    def feed(self, k, img):
        self.k = k
        self.tInit = time.time()
        self.i = img

    def empty(self):
        self.i = 0
        self.k = None
        self.tInit = 0

    def getTime(self):
        t= round(time.time() - self.tInit, 2)
        intt = int(t)
        f = t - intt
        if f <=.13:
            return intt
        elif f<= .38:
            return (intt + .25)*100
        elif f <= .63:
            return (intt + .5)*100
        elif f <= .83:
            return (intt + .75)*100
        else:
            return (intt + 1) * 100

    def isEmpty(self):
        if self.k is None:
            return True
        else:
            return False


def get_data():
    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        image_data = list(np.load(file_name, allow_pickle=True))
        targets = list(np.load(file_name2, allow_pickle=True))
    else:
        print('File does not exist, starting fresh!')
        image_data = []
        targets = []
    return image_data, targets


def save_data(image_data, targets):
    np.save(file_name, image_data)
    np.save(file_name2, targets)


image_data, targets = get_data()
wc = WindowCapture("ArcheAge")
while True:
    keys = key_check()
    print("waiting press B to start")
    if keys == "B":
        print("Starting")
        break

count = 0
#hsvfilter = HsvFilter(14, 0, 0, 179, 255, 255, 0, 0, 0, 45, 1, 3, 2, 128, 100, 1, 3)
vision = Vision()
cv2.namedWindow("AI Peak")
cv2.moveWindow("AI Peak", x=-1920, y=0)
lastKey= KeyData()
while True:
    count += 1
    last_time = time.time()
    image = wc.getScreenshot(region={
        "x": 278,
        "y": 10,
        "w": 1437,
        "h": 775
    })
    image = cv2.resize(image, (368,193))
    #image = vision.apply_hsv_filter(image, hsvfilter)
    # Debug line to show image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("AI Peak", image)
    cv2.waitKey(1)

    # Convert to numpy array

    kRef = key_check()
    if kRef == "H":
        break

    image = np.array(image)
    image_data.append(image)
    targets.append(kRef)
    if kRef == ",":
        kRef = "Z"
    print('{} loop took {} seconds'.format(kRef, time.time() - last_time))

save_data(image_data, targets)
