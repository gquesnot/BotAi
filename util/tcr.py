from time import time

import cv2
import pytesseract

from util.pixel import getImgRectangle, applyThresh, applyRegion, applySave

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


class Tcr:
    def __init__(self, game):
        self.game = game
        self.textConfig = r'-l eng --tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --oem 3 --psm 8'
        self.numberConfig = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6 outputbase digits'

    def initScan(self, region , save):
        img = self.game.screenShot
        img = applyRegion(img, region)
        applySave(img, save)
        return img

    def scanText(self, region=None, save=None):
        img = self.initScan(region, save)

        return [img, pytesseract.image_to_string(img, config=self.textConfig).replace("\n", "").replace("\x0c", "")]

    def scanNumber(self, region=None, save=None):
        img = self.initScan(region, save)
        text = pytesseract.image_to_string(img, config=self.numberConfig).replace("\n", "").replace("\x0c", "")

        print(save, text)
        return img, text
