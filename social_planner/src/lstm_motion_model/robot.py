import lstm_motion_model.robot_utils
from lstm_motion_model import rrt as rrt
#import lstm_motion_modeli.rrt rrt_kinematic_2 as rrt

import matplotlib.pyplot as plt
import numpy as np

class Robot():
    '''class container for robot type
    robots boundry is square and is set by min_x --  ped max_x ped
    
    '''
    def __init__(self, pos, goal_pos, ped_buf = 0.2):      #pos[x,y], goal_pos[x,y]
        self.speed = 2
        self.x = pos[0]
        self.y = pos[1]
        self.theta = 0 #need a way to calculate this
        self.goal_x = goal_pos[0]
        self.goal_y = goal_pos[1]
        self.boundry_x= 10
        self.boundry_y= 10
        self.idx = 0;
        self.ped_buf = ped_buf

        #TODO add check for sane x,y pos


    def SetSpeed(self, ped_seq):
        self.speed = lstm_motion_model.robot_utils.CalcSpeed(ped_seq)
        print("speed", self.speed)
        return self.speed

    def UpdatePos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.theta = pos[2]

    def GetPos(self):
        pos = [slef.x, self.y, self.theta]
        return pos
    
    def UpdateGoal(self, goal_pos):
        self.goal_x = goal_pos[0]
        self.goal_y = goal_pos[1]

    def GetGoal(self):
        goal = [self.goal_x, self.goal_y]
        return goal


#this method will eventualy call the rrt algorithm to create a path/paths
#it will then convert into a friendly form for the rnn model
    def GeneratePath(self, positions, reed_shepp=True): 
        '''create rrt map using pedestrian positions and boundries
            #create bounries as walls -> from 
            # 
            #       (minX,maxY)-----------------(maxX,maxY)
            #            |                           | 
            #            |                           | 
            #            |                           | 
            #            |                           | 
            #            |                           | 
            #            |                           | 
            #       (minX,minY)-----------------(maxX,minY)
            #
        #call rrt path solver with goal_pos
        #convert solution into x, y slices to match speed
            #may not be so trivial
        generates path based on snap shot of pedestrians
        :param positions: list pedestrians positions at call time
            '''
        ##convert to list
        #positions = positions_tensor.cpu()
        #sanity check
        ped, dims = positions.shape
        if dims != 2:
            raise ValueError("pedestrian dimension incorrect")

        show_animation = False

        self.SetBoundry(positions)

        obstacles = lstm_motion_model.robot_utils.CreateObstacleList\
        (positions, self.ped_buf);

        #self.goal_x = 7.19758
        #self.goal_y = 0.629032


#RRT ReedShepp
        if reed_shepp:
            max_iter = 200
            start=[self.x,self.y, np.deg2rad(0)]
            goal = [self.goal_x,self.goal_y, np.deg2rad(-90.0)]
            #rand_area is [min_x, max_x, min_y, max_y]
            RRT = rrt.RRTStarReedsShepp(start=start,goal=goal,
                      obstacle_list=obstacles,
                      rand_area=[-self.boundry_x,self.boundry_x, -self.boundry_y, self.boundry_y],
                      max_iter=max_iter, step_size=0.2)
            path = RRT.planning(animation=show_animation)
            #paths.append(path)

            if path is None:
                print("cannot find path")
                return
            else:
                RRT.draw_graph()
                plt.suptitle('RRT path', fontsize=12)
                plt.xlabel('X(m)')
                plt.ylabel('Y(m)')
                plt.plot([x for (x,y,yaw) in path], [y for (x,y,yaw) in path], 'r')
                plt.grid(True)
                plt.pause(0.1)
                plt.show()
                #plt.draw()

        else:
#Vanilla RRT
            RRT = rrt.RRT(start=[self.x,self.y, self.theta],
                      goal = [self.goal_x,self.goal_y],
                      rand_area=[-15, 15],
                      obstacle_list=obstacles,
                      expand_dis=3)

            path = RRT.planning(animation=show_animation)
            if path is None:
                print("cannot find path")
            else:
                print("found path")
                if show_animation:
                    RRT.draw_graph()
                    plt.plot([x for (x,y) in path], [y for (x, y) in path], '-r')
                    plt.grid(True)
                    plt.pause(0.01)
                    plt.show()

        #assuming proper ammount of steps TODO
        return_path = []
        path.reverse()
            
        return path 
        ''' calls controlles, control for actioning path. path given as set of x,y,theta
        robot uses simple PID control to drive speed and angle of robot. path
        published over twist'''

    def GeneratePathFake(self, seq):
        #faking path generation to allow for prelim testing
        # just get a pedestrians path and transform to = robot path
        # have a look at lstm_motion_model.utils.random_flip_tensor(seq))
        #find an average speed for the robot (change in distance per frame) based on
        #data input given to model
        path = lstm_motion_model.robot_utils.FakePath(seq)
        return path

    def UpdateRobotIdx(self, idx):
        self.idx = idx
        print("robot idx", idx)
        

    def SetBoundry(self, positions):
        '''sets the boundry for rrt
        param: positions is list of pedestrian positions at
        particular time frame, needs to be converted to list'''
        max_x = -1000
        max_y = -1000
        for ped in positions:
            if abs(ped[0]) > max_x:
                max_x = ped[0]
            if abs(ped[1]) > max_y:
                max_y = ped[1]
            
            #for i in range(len(positions[0])):
            #    if ped[i] > max_val:
            #        max_val = ped[i]
            #    elif ped[i] < min_val:
            #        min_val = ped[i]
            #    else:
            #        continue
        #infalte the boundry to allow robot to go around outside
        self.boundry_x= float(max_x) + 2 
        self.boundry_y= float(max_y) + 2 
        print("boundries", self.boundry_x, self.boundry_y)

    
#DEPRECIATED
    #path = self.GeneratePathFake(ped_seq)
   # print("the paths ", paths)
    #convert path into tensor of shape [seq, 1, 2] where seq = path
    # discretised by the speed such that each seq is length/speed
    #testing
    #need final path as [seq_len][dims] to cat into pos_seq for nn
   # steps = (path_len/self.speed)
   ## print("steps", steps)
   # final_path = []
   # step_old = path[0]
   ## print("step_old",step_old)
   # final_path.append(step_old)
   # for i in range(1, path_len):
   #     diff_vect = [(path[i][0] - path[i-1][0])/steps, \
   #           (path[i][1] - path[i-1][1])/steps]
   ##     print("diff_vect", diff_vect)
   #     for j in range(int(steps)): #seqs
   #        # step = [paths[0][i][0] + diff_vect[0], \
   #        #     paths[0][i][1] + diff_vect[1]]
   #         step = [step_old[0] + diff_vect[0], step_old[1] + diff_vect[1]]
   ##         print("step", step)
   #         final_path.append(step)
   #         step_old = step
   #     step_old = path[i]

   # print("len of final ",len(final_path))
   # #reverse so back in correct (start-finish)
   # final_path.reverse()
   # print("final path",final_path)

    
