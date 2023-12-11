# EMG/IMU Gaming
Authors: Aditi Vinod & Ian Walsh

A model that takes in EMG and IMU inputs from armband-collected data and can turn those into keyboard inputs for a video game (ex: Minecraft).

## Current Implemented Commands 
| Forwards (W Key) | Left (A Key) | Backwards (S Key) | Right (D Key) | Punch (Left Mouse) |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ![forwards](https://github.com/aditivinod/emg-imu-gaming/assets/28767801/824d313c-50b1-4d07-890e-6426a0284666) | ![left](https://github.com/aditivinod/emg-imu-gaming/assets/28767801/a23e56af-1f78-4c75-9e4d-49349d51a677)| ![backwards](https://github.com/aditivinod/emg-imu-gaming/assets/28767801/1320682c-91a1-41a7-aeda-10524fa9369c)| ![right](https://github.com/aditivinod/emg-imu-gaming/assets/28767801/ecbfd136-f44c-49dd-b558-093c903338de)| ![punch](https://github.com/aditivinod/emg-imu-gaming/assets/28767801/b04d9cab-2a16-40b7-a634-015c7350750a)|


# Dependencies
- pylsl - `pip install pylsl`
- numpy - `pip install numpy`
- pynput - `pip install pynput`

# Available Scripts
`dual.py` - Main script for running live classification from 2 streams. 

# Helper Scripts
`keyboard_output.py` - Controller for the keyboard & mouse.
