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
    print("here");
    # Figure out if we are using matlab engine or python engine
    # parser = argparse.ArgumentParser(
    #     prog='testDataPython',
    #     description='Run the data testing ')
    # parser.add_argument('--matlabmodel', help='Location of the runModel.m file')
    # parser.add_argument('--pythonmodel', help='Location of the runModel.py file')
    # parser.add_argument('--online', action='store_true', help="Whether to run for head to head battle")
    # args = parser.parse_args()
    # assert args.matlabmodel or args.pythonmodel, 'Please specify a model to run'
    # if args.matlabmodel:
        # try:
        #     import matlab.engine
        # except ImportError:
        #     print('Matlab engine not found. If using MATLAB, please install matlab engine for python')
        # eng = matlab.engine.start_matlab()
        # # if we have a matlab engine and want to use a matlab model, import it
        # pth = os.path.dirname(args.matlabmodel)
        # eng.addpath(pth)
        # runModel = lambda data: eng.runMatlabModel(data)
    # else:
    #     print('no matlab')
    #     dir_path = os.path.dirname(args.pythonmodel)
    #     sys.path.append(dir_path)
    #     from runPythonModel import RunPythonModel 
    #     pml = RunPythonModel(args.pythonmodel)
    #     runModel = lambda data: pml.get_rps(data)

    recv = None
    clear()
    # Find the wristband stream
    stream_name = None
    while not stream_name:
        streams = resolve_stream()
        for i, stream in enumerate(streams):
            print(f"\033[1m{i}: {stream.name()}\033[0m")
        inp = input('Which stream is your EMG wristband? (r) to reload list of available/ (q) to quit')
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

    stream_name2 = None
    while not stream_name2:
        streams2 = resolve_stream()
        for i2, stream2 in enumerate(streams2):
            print(f"\033[1m{i2}: {stream2.name()}\033[0m")
        inp2 = input('Which stream is your IMU wristband? (r) to reload list of available/ (q) to quit')
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

    # Launch listener for the EMG wristband stream
    wrapper = PyLSLWrapper(stream_name)
    wrapper.launch_stream_listener()
    clear()

    # Launch listener for the IMU wristband stream
    wrapper2 = PyLSLWrapper(stream_name2)
    wrapper2.launch_stream_listener()
    clear()


    # inferred_markers = StreamInfo(f'inferred {stream_name}', 'markers', 1, 0)
    # inferred_out = StreamOutlet(inferred_markers)
    # # Watch for the marker stream and create the inference stream 
    # if args.online:
    #     _ = input("Press enter when the marker thread has been launched")
    #     marker_streams = resolve_stream()
    #     for stream in marker_streams:
    #         if stream.name() == 'marker_send':
    #             recv = StreamInlet(stream)
    #             print('Found marker stream')
    #     if not recv:
    #         print('No marker stream found. Make sure there is a computer with a marker stream running')
    #         sys.exit(0)
    #     clear() 

    while True:
        # if args.online:
        #     marker, timestamp = recv.pull_sample()
        # else:
        # inp = input('Press enter to record for inference, q+enter to quit!')
        # if inp == '':
        #     marker = [1]
        # elif inp == 'q':
        #     exit_program()
        #     sys.exit(0)
        marker[0] = 1

        if marker[0] == 1:
            tstamp = time.time()
            # print('3\r')
            # time.sleep(1)
            # print('2\r')
            # time.sleep(1)
            # print('1\r')
            # time.sleep(.5)
            tstamp_start = wrapper.get_curr_timestamp()
            time.sleep(.05)
            # print('Shoot!')
            # time.sleep(2)
            data = wrapper.get_data_from(tstamp_start)
            print(data)
            # inference = runModel(data)
            # inferred_out.push_sample([inference])
            # print(f'Inference: {inference}')
        elif marker==99:
            sys.exit(0)
