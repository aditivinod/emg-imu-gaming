# pip install keyboard
import keyboard

def movement_press(mov):
    """
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
    Releases any movement keys currently being 'pressed.' 

    Movement keys are defined as "w," "a,", "s," and "d." 
    """
    movement_keys = ["w", "a", "s", "d"]
    keyboard.release(movement_keys)


def keyboard_presser_tester():









