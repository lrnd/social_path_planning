import math
import torch
import numpy as np

def CalcSpeed(sample_seq): #sample_seq[seq_len, num_people, dim(x,y)]
    '''
    find the speed of the average pedestrian
    :param sample_seq: a sample of the original seq data
        or some recorded data
    '''
    seq_len, num_p, dims = sample_seq.shape
    if seq_len <= 0 or num_p <= 0 or dims <= 0:
        print("Error sample_seq not valid")
        return
    if num_p < 10:
        #do only up to 10
        samples = num_p
    else:
        samples = 10
    if seq_len > 200:
        sample_len = 200
    else:
        sample_len = seq_len

    sums = 0.00;
    speed_avgs = 0.00
    avg_speed_all = 0.00
    for i in range(1, samples):
        for j in range(2, sample_len):
            sums += CalcDist(sample_seq[j-1][i][0], sample_seq[j][i][0],
            sample_seq[j-1][i][1], sample_seq[j][i][1])

        speed_avgs += sums/sample_len

    avg_speed_all = speed_avgs/samples

    speed = float(avg_speed_all)
    return speed

def CalcDist(x1,x2,y1,y2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return float(dist)


def FakePath(x):
     '''Flip a tensor of x,y points about the x and/or y axis randomly
 
     Accepts any tensor who's final dimension has a size of 2. All leading
     dimensions are collapsed prior to the flip and restored afterwards.
     '''

     dim1, dim2, dim3 = x.shape

     path = x[:,1,:]
     path = path.view(dim1,1,dim3)
     path_shape = path.shape

     if dim3 != 2:
         raise ValueError('Can only rotate x if last dimension has size 2')
 
     flip = torch.bernoulli(torch.tensor([0.5, 0.5])).to(torch.bool)
     coef = torch.ones(2, device=x.device)
     coef[flip] = -1
     return path*coef

def CreateObstacleList(positions, radius):
    '''creates a list of obstacles (x, y, radius)
    from positions of pedestians at time of call for use in path planning 
    positions is one sequence of (num_ped, dims)
    '''
    obstacles = []
    #num_ped, dims = positions_tensor.shape
    #positions = positions_tensor.cpu()
    dims = len(positions[0]);
    if dims != 2:
        raise Exception("incorrect number of dimensions")
        #TODO update to float??
    for ped in positions:
        obstacle = ((float(ped[0]), float(ped[1]), radius))
        obstacles.append(obstacle)
    return obstacles


# This file is from IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>, basic PID
# controller
import time

class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

        .. figure:: images/pid_1.png
           :align:   center

           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """
        error = self.SetPoint - feedback_value

        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time
