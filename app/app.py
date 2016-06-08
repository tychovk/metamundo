#!usr/bin/env python3

import random
import time
from celery.task import PeriodicTask
from datetime import timedelta
from . import cel_app
import math

class WorldGrid:
    def __init__(self):
        '''
        The only information the grid has, is if it's occupied or not.
        '''
        self.x_bounds = [0,1200]
        self.y_bounds = [0,1200]
        self.coords = {x: {y: None for y in range(self.x_bounds[1])} 
                        for x in range(self.y_bounds[1])}
        self.date = 0


class BlobManager:
    def __init__(self, world_grid):
        first_blob_coords = [random.randrange(0, world_grid.x_bounds[1]), 
                             random.randrange(0,world_grid.y_bounds[1])]
        self.blob_id = 1
        self.day = 0
        self.blob_dict = {self.blob_id: {'birthdate': self.day, 
                                    'coords': first_blob_coords}}
        self.blob_id += 1
        



    #@cel_app.task()
    def spawn_blob(self, world_grid):
        '''
        Spawns a new lone blob more than 500 steps away from other blobs
        '''
        self.day += 1
        new_blob_coords = [random.randrange(0, world_grid.x_bounds[1]), 
                                 random.randrange(0,world_grid.y_bounds[1])]

        new_blob_x = random.randrange(0, world_grid.x_bounds[1])
        new_blob_y = random.randrange(0,world_grid.y_bounds[1])

        for blob in self.blob_dict:
            old_blob_x = self.blob_dict[blob]['coords'][0]
            old_blob_y = self.blob_dict[blob]['coords'][1]

            distance = math.sqrt((new_blob_x - old_blob_y)**2 +
                                 (new_blob_y - old_blob_y)**2)

            if distance < 600:
                continue
            self.blob_dict.update({self.blob_id: {'birthdate': self.day,
                                                  'coords': new_blob_coords}})
            self.blob_id += 1
            break

        


class PeriodicTasks(PeriodicTask):
    run_every = timedelta(seconds=5)

    def run(self):
        pass


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


