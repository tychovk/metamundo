from django.db import models

class World(models.Model):
    world_coords = models.TextField(max_length=10000, default='')
    x_lower_bound = models.IntegerField(default=0)
    x_upper_bound = models.IntegerField(default=50)
    y_lower_bound = models.IntegerField(default=0)
    y_upper_bound = models.IntegerField(default=50)
    day = models.IntegerField(default=0)

class Blob(models.Model):
    x = models.IntegerField(default=None)
    y = models.IntegerField(default=None)
    world = models.ForeignKey(World, default=None)

# Create your models here.

