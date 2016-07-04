from django.shortcuts import render, redirect
from app.models import World, Blob
from app.generator import WorldGrid, BlobGenerator
import json
import logging
import re

logging.basicConfig(level=logging.INFO)

def update_session(request, post_value, var_name, val_1, val_2):
    if val_1 in post_value:
        request.session[var_name] = val_1
        return True
    else:
        request.session[var_name] = val_2
        return False

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


    if 'pop_control_override' not in request.session:
        request.session['pop_control_override'] = 'on'

    return render(request, 'control_panel.html', 
                { 'world': world,
                  'blobs': blobs})


def add_blob(request, world_id, override=False):
    world = World.objects.get(id=world_id)
    if request.method == 'POST':
        if request.POST.get('spawn_blob'):
            new_blob = request.POST.get('entered_blob_coords')
        elif request.POST.get('add_blob_at'):
            new_blob = request.POST.get('selected_blob_coords')

        pop_control_value = request.POST.get('override_hidden')
        pop_control = update_session(request, pop_control_value, 'pop_control_override', 'on', 'off')

        logging.info(pop_control)

        '''
        pop_control_button = request.POST.get('override_hidden')
        logging.info (pop_control_button)

        if 'off' in pop_control_button:
            #override = True
            request.session['pop_control_override'] = 'off'
        else:
            #override = False
            request.session['pop_control_override'] = 'on'
        '''
        
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
        x = None
        y = None
        if new_blob:
            new_blob_coords = re.findall("[-+]?\d+", new_blob)
            x = int(new_blob_coords[0])
            y = int(new_blob_coords[1])

        blob_gen = BlobGenerator(world)
        spawn_blob = blob_gen.spawn_blob(new_blob_x=x, new_blob_y=y, 
                                         pop_control=pop_control)


        if spawn_blob:
            x_generated = spawn_blob[0]
            y_generated = spawn_blob[1]

            Blob.objects.create(x=x_generated, y=y_generated, stage=0, 
                                world=world)
            world.status_message = "We have a newcomer! Say hello to your new "\
                                   "little green friend at {x}, {y}." \
                                    .format(x=x_generated, y=y_generated)
            world.save()
        else:
            world.status_message = "The would-be-blob didn't feel so "\
                                   "comfortable popping into existence so "\
                                   "close to other blobs. "\
                                   "Hmm... Maybe a bit farther away."
            world.save()
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

    
def about(request):
    return render(request, 'about.html')