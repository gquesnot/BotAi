import random
import time
import pydirectinput
import keyboard
import time
import cv2
from fastai.vision.all import *

from util.getkeys import key_check
from windowcapture import WindowCapture


def label_func(x): return x.parent.name


def main():
    learn_inf = load_learner("I:/ia/export.pkl")
    print("loaded learner")

    # Sleep time after actions
    sleepy = 0.1

    # Wait for me to push B to start.
    keyboard.wait('B')
    time.sleep(sleepy)

    # Hold down W no matter what!
    # keyboard.press('w')

    # Randomly pick action then sleep.
    # 0 do nothing release everything ( except W )
    # 1 hold left
    # 2 hold right
    # 3 Press Jump
    wc = WindowCapture("ArcheAge")
    cv2.namedWindow("AI Peak")
    cv2.moveWindow("AI Peak", x=-1920, y=0)
    while True:
        image = wc.getScreenshot(region={
            "x": 278,
            "y": 10,
            "w": 1437,
            "h": 775
        })
        image = cv2.resize(image, (368, 193))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("AI Peak", image)
        cv2.waitKey(1)
        # cv2.imshow("Fall", image)
        # cv2.waitKey(1)
        start_time = time.time()
        result = learn_inf.predict(image)
        action = result[0]
        # print(result[2][0].item(), result[2][1].item(), result[2][2].item(), result[2][3].item())
        print(action, result)
        # action = random.randint(0,3)

        if action == "Up":
            keyboard.release("d")
            keyboard.release("q")
        if action == "Left":
            print(f"LEFT! - {result[1]}")
            keyboard.press("q")
            keyboard.release("d")
            time.sleep(sleepy)

        elif action == "Right":
            print(f"Right! - {result[1]}")
            keyboard.press("d")
            keyboard.release("q")

            time.sleep(sleepy)

        # End simulation by hitting h
        keys = key_check()
        if keys == "H":
            break

    keyboard.release('W')


if __name__ == '__main__':
    main()
