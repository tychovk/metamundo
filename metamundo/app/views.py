from django.shortcuts import render, redirect
from app.models import World
from app.generator import WorldGrid
import json

def home_page(request):
    return render(request, 'home.html')


def control_panel(request):
    return render(request, 'control_panel.html')


def new_grid(request):
    if request.method == 'POST':    
        world_grid = WorldGrid()
        world_coords = json.dumps(world_grid.world_coords)
        world = World.objects.create(world_coords=world_coords)
        return redirect('/grid/{}/'.format(world.id))
    return render(request, 'grid.html')



def view_grid(request, world_id):
    world = World.objects.get(id=world_id)
    return render(request, 'grid.html', {'world': world})