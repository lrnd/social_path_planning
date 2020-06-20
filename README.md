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


note: converting data from spenser tracked msgs to .dense files (as required by
network when training) requires python 2 and Spenser tracking msgs installed


Installation
------------

* Checkout or download this repository

* Install ped_sim simulator from https://code.research.uts.edu.au/uts-cas/dwell-track/pedsim_ros/tree/sean/pedsim
    - need to download sean/pedsim version as contains updates to srvs,
      scenarios and launch files that are necessary. 

Quick Start Guide
-----------------

open a terminal 
* 'cd catkin_ws/src'
* 'ln -s "ped_sim directory"
* 'cd ../'
* 'catkin_make'
* 'roslaunch pedsim_simulator sean.launch'

This should launch the pedestrian simulator as well as the srvs required to get
pedestrian data

open new terminal,
initialise python environment with the required packages
* 'cd social_path_planning'
* 'source source_me.sh'
* 'cd rnn/apg-disp'
* 'social_planner -w model.plk'

If you wish to train you own model follow instructions at
https://code.research.uts.edu.au/10173639/human-motion-rnn. there is a data
directory to store data. Run training phase
in rnn, it will create a directory refering to model and time of creating. 

NOTE functionality to run any model has temporarily been
depreciated as experimentation with apg-displacement model is conducted. 


Information
-----------
As the project uses models from https://code.research.uts.edu.au/10173639/human-motion-rnn
and due to the structure of that project there is a lot of interdependency to
run the inference of the model. For this reason the developments for this
project are living in a very similar environment containing many of the
packages from the human-motion-rnn project. The unique contributions of this
project are
* social_planner/scripts/social_planner
* social_planner/src/robot.py
* social_planner/src/lstm_motion_model/robot_utils.py
* social_planner/src/lstm_motion_model/robot_plots.py
* social_planner/src/lstm_motion_model/rrt.py

as well as modification to the existing files
