import pyautogui
import time


class Jiggler():
    run = True

    def __init__(self):
        pass

    def start_jiggler(self):
        print("working ", self.run)
        self.run = True
        while self.run:
            pyautogui.moveRel(0, 50, duration=1)
            time.sleep(1)

    def stop_jiggler(self):
        self.run = False
        print("utils.run ", self.run)

    def test(self):
        while self.run:
            print("Test")
            time.sleep(1)
