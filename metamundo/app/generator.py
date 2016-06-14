#!usr/bin/env python3

import random
import time
from celery.task import PeriodicTask
from datetime import timedelta
from . import cel_app
import math
import logging
from celery import Task

logging.basicConfig(level=logging.INFO)

class WorldGrid(Task):
    def __init__(self):
        '''
        The only information the grid has, is if it's occupied or not.
        '''
        self.x_bounds = [0,500]
        self.y_bounds = [0,500]
        self.coords = {x: {y: None for y in range(self.x_bounds[1])} 
                        for x in range(self.y_bounds[1])}
        self.day = 0



class BlobManager:
    def __init__(self, world_grid):
        self.blob_id = 1
        self.day = 0
        self.blob_dict = {}
        
        
    def coords_gen(self, world_grid):
        x_bounds = world_grid.x_bounds
        y_bounds = world_grid.y_bounds
        new_coords = [random.randrange(x_bounds[0], x_bounds[1]), 
                      random.randrange(y_bounds[0], y_bounds[1])]
        return new_coords


    def spawn_blob(self, world_grid):
        '''
        Spawns a new lone blob more than 200 steps away from other blobs.
        Returns True if blob was spawned
        Returns False if no blob was spawned
        '''

        new_blob_coords = self.coords_gen(world_grid)
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

        
    def start(self, world_grid):
        self.spawn_blob(world_grid)
        self.time_progression()
        #spawn_blob(self, world_grid)


class Player:
    def __init__(self, world_grid, name, x = None, y = None):
        self.name = name
        if x is None:
            x_min = world_grid.x_bounds[0]
            x_max = world_grid.x_bounds[1]
            y_min = world_grid.y_bounds[0]
            y_max = world_grid.y_bounds[1]
            self.x = random.randrange(x_min, x_max)
            self.y = random.randrange(y_min, y_max)


"""

class PeriodicTasks(PeriodicTask):
    run_every = timedelta(seconds=5)

    def run(self):
        pass

"""
