from pylsl import resolve_stream, StreamInfo, StreamOutlet, StreamInlet
from get_lsl_data import PyLSLWrapper, get_all_streams
import random
import sys
import threading
import os
import time
import numpy as np
import atexit
import argparse
from pynput.keyboard import Key, Controller
import keyboard_output

keyboard = Controller()

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

def wfl(input_channel):
    prev = 0
    wfl_out = 0
    for x in input_channel:
        wfl_out += x - prev
        prev = x
    return int(wfl_out / 1000)

"""
Main function to run the program
"""
if __name__=='__main__':
    #Load matlab model
    # eng = matlab.engine.start_matlab()
    # if we have a matlab engine and want to use a matlab model, import it
    # pth = os.path.dirname("./runMatlabModel.m")
    # eng.addpath(pth)
    # runModel = lambda data: eng.runMatlabModel(data)
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

    emgData = PyLSLWrapper(stream_name2)
    emgData.launch_stream_listener()

    clear()
    #wait for data to populate
    time.sleep(1)
    hold = 0
    while True:
        imu_Data = imuData.get_data_from(imuData.get_curr_timestamp()- 0.5)
        emg_Data = emgData.get_data_from(emgData.get_curr_timestamp() - 0.1)

        
        # print(emgData.get_curr_timestamp())
        # fft1 = np.fft.rfft(emg_Data[:,1])
        # fft2 = np.fft.rfft(emg_Data[:,2])
        # fft3 = np.fft.rfft(emg_Data[:,3])
        # fft4 = np.fft.rfft(emg_Data[:,4])
        # punch = int(np.sum(np.abs(fft4)) / 100000000) + int(np.sum(np.abs(fft2)) / 100000000) + int(np.sum(np.abs(fft3)) / 100000000) + int(np.sum(np.abs(fft4)) / 100000000)
        # punch = int(np.sum(np.abs(fft4)) / 100000000)
        print(wfl(emg_Data[:,1]))
        # print(punch)
        punch = wfl(emg_Data[:,1])
        if(punch > 8341):
            keyboard_output.mouse_press(0)
        else:
            keyboard_output.mouse_release()

        #keyboard inputswww
        if(imu_Data[-1][1] > 4):
            keyboard_output.movement_press(1)
        else:
            keyboard.release('a')

        if(imu_Data[-1][1] < -7):
            keyboard_output.movement_press(3)
        else:
            keyboard.release('d')

        if(imu_Data[-1][2] > 3):
            keyboard_output.movement_press(2)
        else:
            keyboard.release('s')

        if(imu_Data[-1][2] < -2):
            keyboard_output.movement_press(0)
        else:
            keyboard.release('w')
        
        # inference = runModel(data)
        # inferred_out.push_sample([inference])
        # print(f'Inference: {inference}')

        time.sleep(.01)
