
from mss import mss
from mss.base import MSSBase
from numpy import ndarray, array
from cv2 import imread, matchTemplate, minMaxLoc, cvtColor, TM_CCOEFF_NORMED, IMREAD_COLOR
from cv2.typing import Point
from mouse import click, move, on_right_click, LEFT

MONITOR: tuple[int, int, int, int] = (0, 0, 1920, 1080)

SUCCESSFUL_MATCHED_PERCENT: float = .8

BANANA_IMAGE: ndarray = imread('banana.png', IMREAD_COLOR)

BANANA_HALF_WIDTH: int = round(BANANA_IMAGE.shape[1] / 2)
BANANA_HALF_HEIGHT: int = round(BANANA_IMAGE.shape[0] / 2)

class Status():
    def __init__(self):
        self.__is_runing = True

    def stop(self) -> None:
        self.__is_runing = False

    def is_runing(self) -> bool:
        return self.__is_runing

def make_screenshot(base: MSSBase) -> ndarray:
    return cvtColor(array(base.grab(MONITOR)), IMREAD_COLOR)

def match_one(image: ndarray, haystack: ndarray) -> Point | None:
    result: ndarray = matchTemplate(image, haystack, TM_CCOEFF_NORMED)
    _, maxVal, _, maxLoc = minMaxLoc(result)
    if maxVal >= SUCCESSFUL_MATCHED_PERCENT:
        return maxLoc

    return None

def get_banana(screenshot: ndarray) -> Point | None:
    point = match_one(BANANA_IMAGE, screenshot)
    if point is not None:
        return point

    return None

def banana() -> None:
    status: Status = Status()
    on_right_click(status.stop)

    base: MSSBase = mss()
    banana: Point | None = None

    while status.is_runing():
        if banana == None:
            screenshot: ndarray = make_screenshot(base)
            banana: Point | None = get_banana(screenshot)
        
        if banana != None:
            move(
                banana[0] + BANANA_HALF_WIDTH, 
                banana[1] + BANANA_HALF_HEIGHT
            )

            click(LEFT)
 
if __name__ == "__main__":
    banana() 
