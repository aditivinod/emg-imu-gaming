# pip install keyboard``
#import keyboard
import time

from pynput.keyboard import Controller
keyboard = Controller()

def movement_press(mov):
    """w
    Given an output indicating the direction of movement from the IMU model,
    outputs the corresponding key to move in that direction.

    The movement is as follows: "w" for forwards, "a" for left, "s" for s
    backwards, and "d" for right. The default 

    Args:
        mov: Output from IMU live classification determining which direction to
            move in.
    """
    match mov:
        case 0:
            keyboard.press("w")
            print("Press")
        case 1:
            keyboard.press("a")
        case 2:
            keyboard.press("s")
        case 3:
            keyboard.press("d")
        case _:
            movement_release()
        
def movement_release():
    """
    Releases any movement keys currently being 'pressed.' #

    Movement keys are defined as "w," "a,", "s," and "d." 
    """
    movement_keys = ["w", "a", "s", "d"]
    for key in movement_keys:
       keyboard.release(key)
    print("Release")

while True:
    movement_press(0)
    time.sleep(0.5)
    movement_release()
    if keyboard.read_key() == "x":
        print("Exiting")
        break
