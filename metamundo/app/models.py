from django.db import models

class World(models.Model):
    world_coords = models.TextField(max_length=10000, default='')

class Blob(models.Model):
    blob_coords = models.TextField(max_length=10000, default='')
    world = models.ForeignKey(World, default=None)




# Create your models here.

