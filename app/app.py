#!usr/bin/env python3

import random

class WorldGrid:
    def __init__(self):
        '''
        The only information the grid has, is if it's occupied or not.
        '''
        self.coords = {x: {y: None for y in range(20)} for x in range(20)}
        self.x_bounds = [0,20]
        self.y_bounds = [0,20]

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

