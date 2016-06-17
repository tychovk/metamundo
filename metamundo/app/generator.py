#!usr/bin/env python3

import random
import time
from celery.task import PeriodicTask
from datetime import timedelta
from . import cel_app
import math
import logging
from celery import Task
import json




logging.basicConfig(level=logging.INFO)

class WorldGrid(Task):
    def __init__(self):
        '''
        The only information the grid has, is if it's occupied or not.
        '''
        self.x_bounds = [0,50]
        self.y_bounds = [0,50]
        self.grid_coords = [[x, y] for x in range(self.x_bounds[1]) 
                                    for y in range(self.y_bounds[1])]

        self.coords = {x: {y: None for y in range(self.x_bounds[1])} 
                        for x in range(self.y_bounds[1])}
        self.world_coords = json.dumps(self.coords)
        self.day = 0
        self.blob_id = 1
        self.blob_dict = {}
        
        
    def coords_gen(self):
        x_bounds = self.x_bounds
        y_bounds = self.y_bounds
        new_coords = [random.randrange(x_bounds[0], x_bounds[1]), 
                      random.randrange(y_bounds[0], y_bounds[1])]
        return new_coords


    def spawn_blob(self):
        '''
        Spawns a new lone blob more than 200 steps away from other blobs.
        Returns True if blob was spawned
        Returns False if no blob was spawned
        '''

        new_blob_coords = self.coords_gen(self.world_coords)
        new_blob_x = new_blob_coords[0]
        new_blob_y = new_blob_coords[1]

        for blob in self.blob_dict:
            old_blob_x = self.blob_dict[blob]['coords'][0]
            old_blob_y = self.blob_dict[blob]['coords'][1]

            distance = math.sqrt((new_blob_x - old_blob_x)**2 +
                                 (new_blob_y - old_blob_y)**2)

            if distance <= 200:
                return False

        self.blob_dict.update({self.blob_id: {'birthdate': self.day,
                                                  'coords': new_blob_coords}})
        self.blob_id += 1

        return True


   #@cel_app.task(name="time_progression")
    def time_progression(self):
        self.day += 1
        print (self.day)
        return

        
    def start(self):
        self.spawn_blob()
        self.time_progression()
        #spawn_blob(self)


class Player:
    def __init__(self, name, x = None, y = None):
        self.name = name
        if x is None:
            x_min = self.x_bounds[0]
            x_max = self.x_bounds[1]
            y_min = self.y_bounds[0]
            y_max = self.y_bounds[1]
            self.x = random.randrange(x_min, x_max)
            self.y = random.randrange(y_min, y_max)








"""

class PeriodicTasks(PeriodicTask):
    run_every = timedelta(seconds=5)

    def run(self):
        pass

"""
