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
from app.models import World, Blob 



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


class BlobGenerator:
    def __init__(self, world):
        self.x_lower_bound = world.x_lower_bound
        self.x_upper_bound = world.x_upper_bound
        self.y_lower_bound = world.y_lower_bound
        self.y_upper_bound = world.y_upper_bound
        self.world = world

    def coords_gen(self, x=None, y=None):
        new_coords = [random.randrange(self.x_lower_bound, self.x_upper_bound), 
                      random.randrange(self.y_lower_bound, self.y_upper_bound)]
        return new_coords


    def spawn_blob(self, new_blob_x=None, new_blob_y=None, pop_control=True):
        '''
        Spawns a new lone blob more than 200 steps away from other blobs.
        Returns True if blob was spawned
        Returns False if no blob was spawned
        '''
        
        blob_coords = tuple((blob.x, blob.y) \
                      for blob in Blob.objects.all().filter(world=self.world))

        if new_blob_x is None or new_blob_y is None:
            new_blob_coords = self.coords_gen()
            new_blob_x = new_blob_coords[0]
            new_blob_y = new_blob_coords[1]

        for old_blob in blob_coords:
            old_blob_x = old_blob[0]
            old_blob_y = old_blob[1]

            distance = math.sqrt((new_blob_x - old_blob_x)**2 +
                                 (new_blob_y - old_blob_y)**2)

            if distance <= 20 and pop_control is True:
                return False

        return (new_blob_x, new_blob_y)

# generate blob, add birthday, etc



"""

class PeriodicTasks(PeriodicTask):
    run_every = timedelta(seconds=5)

    def run(self):
        pass

"""
