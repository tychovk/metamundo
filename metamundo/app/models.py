from django.db import models

class World(models.Model):
    world_coords = models.TextField(max_length=10000, default='')

class Blob(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    world = models.ForeignKey(World, default=None)




# Create your models here.

