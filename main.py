import time
import pyautogui
from mss import mss
from numpy import ndarray, array
from cv2 import imread, matchTemplate, minMaxLoc, cvtColor, TM_CCOEFF_NORMED, IMREAD_COLOR
from cv2.typing import Point
from mouse import move, on_right_click, LEFT

MONITOR = (0, 0, 1920, 1080)
SUCCESSFUL_MATCHED_PERCENT = .8
BANANA_IMAGE = imread('\\full\\path\\to\\banana.png', IMREAD_COLOR)
BANANA_HALF_WIDTH = round(BANANA_IMAGE.shape[1] / 2)
BANANA_HALF_HEIGHT = round(BANANA_IMAGE.shape[0] / 2)

class Status:
    def __init__(self):
        self.__is_runing = True

    def stop(self):
        self.__is_runing = False

    def is_runing(self):
        return self.__is_runing

def make_screenshot(base):
    return cvtColor(array(base.grab(MONITOR)), IMREAD_COLOR)

def match_one(image, haystack):
    result = matchTemplate(image, haystack, TM_CCOEFF_NORMED)
    _, maxVal, _, maxLoc = minMaxLoc(result)
    if maxVal >= SUCCESSFUL_MATCHED_PERCENT:
        return maxLoc
    return None

def get_banana(screenshot):
    return match_one(BANANA_IMAGE, screenshot)

def banana():
    status = Status()
    on_right_click(status.stop)
    base = mss()

    while status.is_runing():
        banana = get_banana(make_screenshot(base))
        if banana:
            move(banana[0] + BANANA_HALF_WIDTH, banana[1] + BANANA_HALF_HEIGHT)
            pyautogui.click(clicks=30, interval=1/30)
 
if __name__ == "__main__":
    banana()
