from django.shortcuts import render, redirect
from app.models import World, Blob
from app.generator import WorldGrid
import json
import logging

logging.basicConfig(level=logging.INFO)


def home_page(request):
    return render(request, 'home.html')


def new_world(request):
    world_grid = WorldGrid()
    world_coords = world_grid.world_coords
    world = World.objects.create(world_coords=world_coords)
    return redirect('/world/{}/'.format(world.id))


def view_world(request, world_id):
    world = World.objects.get(id=world_id)
    world_coords = None
    if hasattr(world, 'world_coords'):
        world_coords = json.loads(world.world_coords) # what is going on here
    blobs = Blob.objects.all().filter(world=world)
    return render(request, 'control_panel.html', 
                { 'world': world,
                'world_coords': world_coords,
                'blobs': blobs})


def control_panel(request):
    return render(request, 'control_panel.html', {'world': False})


def new_grid(request):
    if request.method == 'POST':    
        world_grid = WorldGrid()
        world_coords = world_grid.world_coords
        world = World.objects.create(world_coords=world_coords)
        return redirect('/grid/{}'.format(world.id))
    return render(request, 'grid.html', {'world': False})



def view_grid(request, world_id):
    world = World.objects.get(id=world_id)
    return render(request, 'grid.html', {'world': world})

    