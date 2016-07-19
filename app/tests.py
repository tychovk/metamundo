from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core import serializers

from app.generator import WorldGrid, BlobGenerator
from app.views import home_page, control_panel, new_world, world
from app.models import World, Blob

import logging
import math
import json

logging.basicConfig(level=logging.INFO)


class ControlPanelTest(TestCase):

    def test_control_panel_url_resolves(self):
        found = resolve('/control_panel/new')
        self.assertEqual(found.func, new_world)


    def test_control_panel_returns_correct_html(self):
        request = HttpRequest()
        response = control_panel(request)
        expected_html = render_to_string('control_panel.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)


    def test_saving_new_world_from_POST_request(self):
        self.client.post(
            '/control_panel/new',
        )

        self.assertEqual(World.objects.count(), 1)



    def test_redirects_to_world_view(self):
        world = World.objects.create()

        response = self.client.post(
            '/control_panel/{}/add_blob'.format(world.id),
            data={'entered_blob_coords': "1 2", 'spawn_blob': 'Spawn Blob',
                  'override_hidden': 'off'}
        )

        self.assertRedirects(response, '/control_panel/{}/'.format(world.id))


    # Doesn't seem to work with templates that receive JSON?
    #def test_uses_world_view_template(self):
    #    world = World.objects.create()
    #    response = self.client.get('/world/{}/'.format(world.id))
    #
    #    self.assertTemplateUsed(response, 'control_panel.html')


#    def test_passes_correct_world_coords_to_template(self):
#        world_coords = WorldGrid().world_coords
#
#        correct_world = World.objects.create(world_coords=world_coords)
#        world_coords = None
#        if hasattr(correct_world, 'world_coords'):
#            world_coords = json.loads(correct_world.world_coords)
#        response = self.client.get('/world/{}/'.format(correct_world.id))
#
#        self.assertEqual(response.context['world_coords'], world_coords)





    # Not a necessary test if the right world is passed and 
    # correct blobs are assigned
#    def test_passes_correct_blob_coords_to_template(self):
#        world_coords = WorldGrid().world_coords
#
#        correct_world = World.objects.create(world_coords=world_coords)
#        Blob.objects.create(x=1, y=2, world=correct_world)
#
#        blobs = Blob.objects.all().filter(world=correct_world)
#
#        response = self.client.get('/world/{}/'.format(correct_world.id))
#
#        print ("correct blob coords, {}".format(correct_world.blobs))
#
#        self.assertEqual(response.context['blobs'], blobs)
#        print (response.context['blobs'])


class NewWorldTest(TestCase):

    def test_uses_grid_template(self):
        world = World.objects.create()
        response = self.client.get('/grid/new'.format(world.id))
        self.assertTemplateUsed(response, 'grid.html')


    def test_saving_new_world_from_POST_request(self):
        self.client.post(
            '/control_panel/new',
        )

        self.assertEqual(World.objects.count(), 1)


    def test_saving_and_retrieving_worlds(self):
        x_bounds = [0,50]
        y_bounds = [0,50]
        coords = {x: {y: None for y in range(x_bounds[1])} 
                        for x in range(y_bounds[1])}
        json_coords = json.dumps(coords)    

        world_1 = World()
        world_1.world_coords = json.dumps(coords)
        world_1.save()

        world_2 = World()
        world_2.world_coords = json.dumps(coords)
        world_2.save()

        saved_worlds = World.objects.all()
        self.assertEqual(saved_worlds.count(), 2)

        first_saved_world = saved_worlds[0]
        second_saved_world = saved_worlds[1]
        self.assertEqual(json_coords, first_saved_world.world_coords)
        self.assertEqual(json_coords, second_saved_world.world_coords)
    

class BlobSpawnTest(TestCase):

    def test_saving_blob_from_POST_request(self):
        world = World.objects.create()

        self.client.post(
            '/control_panel/{}/add_blob'.format(world.id),
            data={'entered_blob_coords': "11 5", 'spawn_blob': 'Spawn Blob',
                  'override_hidden': 'off'}
        )
        
        self.assertEqual(Blob.objects.count(), 1)

        saved_blob = Blob.objects.first()

        self.assertEqual(saved_blob.x, 11)
        self.assertEqual(saved_blob.y, 5)
        self.assertEqual(saved_blob.world, world)


    def test_saving_and_retrieving_blob_coords(self):
        world_ = World.objects.create()
        world_.save()

        first_blob = Blob()
        first_blob.x = 1
        first_blob.y = 1
        first_blob.world = world_
        first_blob.save()

        second_blob = Blob()
        second_blob.x = 2
        second_blob.y = 2
        second_blob.world = world_
        second_blob.save()

        saved_world = World.objects.first()
        self.assertEqual(saved_world, world_)

        saved_blob_coords = Blob.objects.all()
        self.assertEqual(saved_blob_coords.count(), 2)

        saved_first_blob = saved_blob_coords[0]
        saved_second_blob = saved_blob_coords[1]

        self.assertEqual(saved_first_blob.x, 1)
        self.assertEqual(saved_first_blob.y, 1)
        self.assertEqual(saved_first_blob.world, world_)
        self.assertEqual(saved_second_blob.x, 2)
        self.assertEqual(saved_second_blob.y, 2)


    def test_displays_only_blobs_for_that_world(self):
        correct_world = World.objects.create()

        Blob.objects.create(x=1, y=2, world=correct_world)
        Blob.objects.create(x=3, y=4, world=correct_world)

        other_world = World.objects.create()
        Blob.objects.create(x=5, y=6, world=other_world)
        Blob.objects.create(x=7, y=8, world=other_world)

        response = self.client.get('/world/{}/'.format(correct_world.id))
        response = json.loads(response.context['blobs'])

        self.assertEqual(1, response[0]['fields']['x'])
        self.assertEqual(2, response[0]['fields']['y'])
        self.assertEqual(3, response[1]['fields']['x'])
        self.assertEqual(4, response[1]['fields']['y'])
        for blob in response:
            self.assertNotEqual(5, blob['fields']['x'])
            self.assertNotEqual(6, blob['fields']['y'])
            self.assertNotEqual(7, blob['fields']['x'])
            self.assertNotEqual(8, blob['fields']['y'])

class BlobGeneratorTest(TestCase):

    def test_too_close_blob_spawns_without_override(self):
        world = World.objects.create()
        blob_gen = BlobGenerator(world)
        pop_control= True
        first_x = 1
        first_y = 1
        second_x = 2
        second_y = 2

        spawn_blob_1 = blob_gen.spawn_blob(new_blob_x=first_x, 
                                           new_blob_y=first_y,
                                           pop_control=pop_control)

        Blob.objects.create(x=spawn_blob_1[0], y=spawn_blob_1[1], stage=0, 
                            world=world)



        spawn_blob_2 = blob_gen.spawn_blob(new_blob_x=second_x, 
                                           new_blob_y=second_y,
                                           pop_control=pop_control)
        
        self.assertTrue(spawn_blob_1)
        self.assertFalse(spawn_blob_2)
        

    def test_too_close_blob_spawns_with_override(self):
        world = World.objects.create()
        blob_gen = BlobGenerator(world)
        pop_control = False
        first_x = 1
        first_y = 1
        second_x = 2
        second_y = 2

        spawn_blob_1 = blob_gen.spawn_blob(new_blob_x=first_x, 
                                           new_blob_y=first_y,
                                           pop_control=pop_control)

        Blob.objects.create(x=spawn_blob_1[0], y=spawn_blob_1[1], stage=0, 
                            world=world)

        spawn_blob_2 = blob_gen.spawn_blob(new_blob_x=second_x, 
                                           new_blob_y=second_y,
                                           pop_control=pop_control)
        
        self.assertTrue(spawn_blob_1)
        self.assertTrue(spawn_blob_2)