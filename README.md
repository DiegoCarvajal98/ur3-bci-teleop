# ur3-bci-teleop
UR3 robot teleoperation with BCI-SSVEP recorded data

## Dataset
For this project, we're going to use the dataset provided by MAMEM Project [[1]](#references) which offers signals taken from 11 subjects using an Emotiv Epoc BCI with the SSVEP paradigm and 5 stimulus frequencies. The dataset used is:
* [EEG SSVEP Dataset III](https://figshare.com/articles/dataset/MAMEM_EEG_SSVEP_Dataset_III_14_channels_11_subjects_5_frequencies_presented_simultaneously_/3413851)

## EEG Signal Processing Toolbox
To process the EEG data from the datasets, we're going to use the processing toolbox offered by MAMEM Project [[1]](#references).
* [EEG Processing Toolbox](https://github.com/MAMEM/eeg-processing-toolbox)

## Setup
This project has been tested on a Ubuntu 18.04 machine with 16 GB Ram, Intel Core i5-4210U processor and with [ROS Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu) and Matlab 2021b installed.

## ROS Packages
The ROS packages used for this project are:
* (aruco_ros)[https://github.com/pal-robotics/aruco_ros]
* (moveit)[https://moveit.ros.org/install/]
* (universal_robots_ros_driver)[https://github.com/UniversalRobots/Universal_Robots_ROS_Driver]
* (usb_cam)[http://wiki.ros.org/usb_cam]
* (moveit_calibration)[https://github.com/ros-planning/moveit_calibration]
* (ur3)[https://github.com/cambel/ur3]

# References
[[1]](https://www.mamem.eu/) Mamem Project page