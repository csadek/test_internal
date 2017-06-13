import pyautogui
pyautogui.FAILSAFE = False
from time import sleep
import sys


def main(fileName):
    sleep(5)
    pyautogui.typewrite(fileName)
    pyautogui.press('enter')

if __name__ == '__main__':
    main(sys.argv[1])

