from django.shortcuts import render, redirect
from app.models import World, Blob
from app.generator import WorldGrid
import json
import logging

logging.basicConfig(level=logging.INFO)


def home_page(request):
    return render(request, 'home.html')


def new_world(request):
    world = World.objects.create()
    return redirect('/world/{}/'.format(world.id))


def view_world(request, world_id):
    world = World.objects.get(id=world_id)
#    if hasattr(world, 'world_coords'):
#        world_coords = json.loads(world.world_coords) # what is going on here
    blobs = Blob.objects.all().filter(world=world)
    return render(request, 'control_panel.html', 
                { 'world': world,
                'blobs': blobs})


def add_blob(request, world_id):
    world = World.objects.get(id=world_id)
    if request.method == 'POST':
        new_blob = request.POST.getlist('new_blob')
        '''
        # future use
        blobs_query = [
                Blob(
                    x=new_blob[0],
                    y=new_blob[1],
                    world=world,
                )
                for new_blob in new_blobs
        ]
    
        Blob.objects.bulk_create(blobs_query)
        '''
        x = int(new_blob[0])
        y = int(new_blob[1])
        Blob.objects.create(x=x, y=y, world=world)
    return redirect('/world/{}/'.format(world.id))


def control_panel(request):
    return render(request, 'control_panel.html', {'world': False})


def new_grid(request):
    if request.method == 'POST':    
        world = World.objects.create()
        return redirect('/grid/{}'.format(world.id))
    return render(request, 'grid.html', {'world': False})



def view_grid(request, world_id):
    world = World.objects.get(id=world_id)
    return render(request, 'grid.html', {'world': world})

    