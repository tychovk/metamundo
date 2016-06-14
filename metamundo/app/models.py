from django.db import models

class World(models.Model):
    world_coords = models.TextField(max_length=10000, default='')

# Create your models here.

