from pylsl import resolve_stream, StreamInfo, StreamOutlet, StreamInlet
from get_lsl_data import PyLSLWrapper, get_all_streams
from pynput import keyboard
import random
import sys
import threading
import os
import time
import numpy as np
import atexit
import argparse
from pynput.keyboard import Key, Controller

keyboard = Controller()

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
    Releases any movement keys currently being 'pressed.' #

    Movement keys are defined as "w," "a,", "s," and "d." 
    """
    movement_keys = ["w", "a", "s", "d"]
    for key in movement_keys:
       keyboard.release(key)


"""
Helper functions, don't worry about these!
"""
clear = lambda : os.system('cls' if os.name == 'nt' else 'clear')
wrapper = None

def exit_program():
    print('Finished the gestures!')
    print('set!')
    if wrapper:
        wrapper.end_stream_listener(save_file=False)
    sys.exit(0)

atexit.register(exit_program)

"""
Main function to run the program
"""
if __name__=='__main__':
    #Load matlab model
    try:
        import matlab.engine
    except ImportError:
        print('Matlab engine not found. If using MATLAB, please install matlab engine for python')
    eng = matlab.engine.start_matlab()
    # if we have a matlab engine and want to use a matlab model, import it
    pth = os.path.dirname(args.matlabmodel)
    eng.addpath(pth)
    runModel = lambda data: eng.runMatlabModel(data)
    clear()


    # Find the IMU stream
    stream_name = None
    while not stream_name:
        streams = resolve_stream()
        for i, stream in enumerate(streams):
            print(f"\033[1m{i}: {stream.name()}\033[0m")
        inp = input('Which stream is your IMU wristband? (r) to reload list of available/ (q) to quit')
        if inp == 'r': 
            print('Reloading')
            continue
        elif inp == 'q':
            sys.exit(0)
        else:
            try:
                stream_name = streams[int(inp)].name()
                if stream_name == 'marker_send':
                    print('Please choose a different stream')
                    stream_name = None
                    continue
                clear()
            except:
                print('Please enter a valid int listed')

    #Find the EMG stream
    stream_name2 = None
    while not stream_name2:
        streams2 = resolve_stream()
        for i2, stream2 in enumerate(streams2):
            print(f"\033[1m{i2}: {stream2.name()}\033[0m")
        inp2 = input('Which stream is your EMG wristband? (r) to reload list of available/ (q) to quit')
        if inp2 == 'r': 
            print('Reloading')
            continue
        elif inp2 == 'q':
            sys.exit(0)
        else:
            try:
                stream_name2 = streams2[int(inp2)].name()
                if stream_name2 == 'marker_send':
                    print('Please choose a different stream')
                    stream_name2 = None
                    continue
                clear()
            except:
                print('Please enter a valid int listed')

    # Launch listener for the IMU wristband stream
    imuData = PyLSLWrapper(stream_name)
    imuData.launch_stream_listener()

    emgData = PyLSLWrapper(stream_name)
    emgData.launch_stream_listener()

    clear()
    #wait for data to populate
    time.sleep(1)

    while True:
        data = imuData.get_data_from(1)

        #keybaord inputs
        if(data[-1][1] > 4):
            movement_press(1)
        else:
            keyboard.release('a')

        if(data[-1][1] < -7):
            movement_press(3)
        else:
            keyboard.release('d')

        if(data[-1][2] > 3):
            movement_press(2)
        else:
            keyboard.release('s')

        if(data[-1][2] < -2):
            movement_press(0)
        else:
            keyboard.release('w')
        
        # inference = runModel(data)
        # inferred_out.push_sample([inference])
        # print(f'Inference: {inference}')

        time.sleep(.01)
