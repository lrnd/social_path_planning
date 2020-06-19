#social path planner

Social Path Planner
===========================

Requirements
------------
Python 3 with the following packages:

* torch
* numpy
* matplotlib
* sklearn
* ROS, project was tested with ROS melodic

Pedsim-ros-sean project to provide simulation environment

note: converting data from spenser tracked msgs to .dense files (as required by
network when training) requires python 2 and Spenser tracking msgs installed


Installation
------------

* Checkout or download this repository

* Install ped_sim simulator from https://code.research.uts.edu.au/uts-cas/dwell-track/pedsim_ros/tree/sean/pedsim
    - need to download sean/pedsim version as contains updates to srvs,
      scenarios and launch file necessary. 

Quick Start Guide
-----------------

open a terminal 
    'cd catkin_ws/src'
    'ls -s "ped_sim directory"
    'cd ../'
    'catkin_make'
    'roslaunch pedsim_simulator sean.launch'

open new terminal
initialise python environment with required packages
    'cd social_path_planning'
    'source source_me.sh'
    'cd rnn/apg-disp'
    './social_planner -w model.plk'

If you wish to train you own model follow instructions at
https://code.research.uts.edu.au/10173639/human-motion-rnn. Run training phase
in rnn, it will create a directory refering to model and time of creating. Data
in social_path_planner/data is already in .dense formate and does not need to
be prepaired. NOTE functionality to run any model has temporarily been
depreciated as experimentation with apg-displacement model is conducted. 
    
