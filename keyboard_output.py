import time

# pip install pynput
from pynput.keyboard import Key, Listener, Controller as KeyController
from pynput.mouse import Button, Controller as MouseController
keyboard = KeyController()
mouse = MouseController()

exit_flag = False  # Flag to control the loop

def movement_press(mov):
    """
    Given an output indicating the direction of movement from the IMU model,
    outputs the corresponding key to move in that direction.

    The movement is as follows: "w" for forwards, "a" for left, "s" for s
    backwards, and "d" for right. The default 

    Args:
        mov: An integer output from IMU live classification determining which 
        direction to move in.
    """
    match mov:
        case 0:
            keyboard.press("w")
            print("w")
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

def mouse_press(click):
    """
    Given an output indicating the type of mouse button from the EMG model, 
    outputs the corresponding click.

    The clicks are as follows: left click for punching, right click for placing.

    Args:
        click: An integer output from EMG live classification determining which
        mouse action to do. 
    """
    match click:
        case 0: 
            mouse.press(Button.left)
            print("click")
        case 1:
            mouse.press(Button.right)
        case _:
            mouse_release()


def mouse_release():
    """
    Releases any mouse buttons currently being pressed.

    Mouse buttons are currently defined as left click & right click.
    """
    mouse.release(Button.left)
    mouse.release(Button.right)

def mouse_move(dir):
    """
    Moves the mouse by a constant amount (amt) in a given direction.
    
    Note: For this to work, user must have Options > Controls > Mouse Settings 
    > Raw Input: OFF

    Args:
        dir: An integer representing the direction of mouse movement.
    """
    amt = 50
    match dir: 
        case 0:
            print('up')
            mouse.move(0, -amt)
        case 1:
            mouse.move(-amt, 0)
        case 2: 
            print('down')
            mouse.move(0, amt)
        case 3: 
            mouse.move(amt, 0)

def mouse_reset():
    """
    Resets the cursor to the center of the screen, assuming a 1920x1080 pixel
    screen.
    """
    height = 1080
    width = 1920
    print('Current mouse position −> {0}'.format(mouse.position))
    mouse.position = (width/2, height/2)

def on_press(key):
    """
    A function that handles actions on key presses.

    Args:
        key: A Key given from the listener
    """
    global exit_flag
    try:
        if key.char == "x":
            print("Exiting")
            exit_flag = True
    except AttributeError as e:
        print(e)

def on_release(key):
    """
    A function that handles actions on key releases.

    Args:
        key: A Key given from the listener.
    """
    pass

def try_keyboard_output():
    """
    Testing function.
    """
    with Listener(on_press=on_press, on_release=on_release) as listener:
        while not exit_flag:
            # mouse_press(0)
            mouse_move(0)
            time.sleep(0.5)
            mouse_reset()
            # mouse_release()

try_keyboard_output()   

