#code for map generation. cretates boundries and adds obsticles -> inflated
#pedestrians

import numpy as np
from rtree import Rtree

from src.


class map(object):
    def __init__(self, boundries, ped_pos=None, inflate):
        """
        create the search space by creating pedestrian obstacles within
        boundries
        :param boundries: max/min of each dimension in form [(x_low, x_max),
        (y_low, y_max)]-->check
        :param O: list of pedestiran positions
        """
        self.inflate = inflate
        if len(boundries) < 2:
            raise Exception("need 2 dimensions for boundrys")

        if any(len(i) != 2 for i in boundries):
            raise Exception("dimensions can only have start/end")
        if any(i[0] >= i[1] for i in boundries):
            raise Exception("boundry start must be less then end")

        self.dimensions = len(boundries)
        self.boundries = boundries
        #using R-tree representation
        prop = Rtree.Property()
        prop.dimension = self.dimensions
        if ped_pos = None:
            self.obs = Rtree.Index(interLeaved=True, properties=prop)
        else:
            obstacles = createObstacles(self, ped_pos)
            if any(len(o) / 2 != self.dimensions for o in obstacles):
                raise Exception("obstacle has incorrect dimension")
            if any(o[i] >= o[int(i+len(o)/2)] for o in obstacle for i in \
            range(int(len(o) / 2))):
                raise Exception("obstacle has incorrect dimension definition")
            self.obs = Rtree.Index(obstacleGenerator(obstacles, \
            interleaved=True, properties=prop)


    def createObstacles(self, ped_pos):
        """
        create obstacles from pedestrian displacements
        :param ped_pos: list of pedestrian displacements
        """
        #ped_pos = [num_ped][x/y]
        obstacles = []
        num_ped, dims = ped_pos.shape
        min_xy = np.empty(self.dimensions, np.float)
        max_xy = np.empty(self.dimensions, np.float)
        for i in (num_ped):
            for j in range(self.dimensions):
                min_xy[j] = ped_pos[num_ped][j] - self.inflate/2
                max_xy[j] = ped_pos[num_ped][j] + self.inflate/2
            obstacle = np.append(min_xy, max_xy)
            #check boundries TODO
            #remove any pedestrians not within boundries
            obstacles.append(obstacle)

        print obstacles 
        return obstacles
            
    def obstacleGenerator(obstacles):
        """
        add obstacles to r-tree
        :param obstacles: list of obstacles
        """
        for obstacle in obstacles:
            yield (uuid.uuid4(), obstacle, obstacle)
            
    def obstacle_free(self, x):
          """ 
          Check if a location resides inside of an obstacle 
          :param x: location to check
          :return: True if not inside an obstacle, False otherwise 
          """ 
          return self.obs.count(x) == 0                                                                
              
      def sample_free(self): 
          """ 
          Sample a location within X_free                                                              
          :return: random location within X_free                                                       
          """
          while True:  # sample until not inside of an obstacle                                        
              x = self.sample()
              if self.obstacle_free(x):                                                                
                  return x
              
      def collision_free(self, start, end, r):
          """
          Check if a line segment intersects an obstacle                                               
          :param start: starting point of line
          :param end: ending point of line                                                             
          :param r: resolution of points to sample along edge when checking for collisions             
          :return: True if line segment does not intersect an obstacle, False otherwise                
          """
          points = es_points_along_line(start, end, r)                                                 
          coll_free = all(map(self.obstacle_free, points))                                             
          return coll_free                                                                             
                                                                                                       
      def sample(self):
          """                                                                                          
          Return a random location within X                                                            
          :return: random location within X (not necessarily X_free)                                   
          """                                                                                          
          x = np.random.uniform(self.dimension_lengths[:, 0], self.dimension_lengths[:, 1])            
          return tuple(x)
        
            
            

