from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.generator import WorldGrid
from app.views import home_page, control_panel, new_world, view_world
from app.models import World, Blob

import logging
import math
import json

logging.basicConfig(level=logging.INFO)


class ControlPanelTest(TestCase):

    def test_control_panel_url_resolves(self):
        found = resolve('/world/new')
        self.assertEqual(found.func, new_world)


    def test_control_panel_returns_correct_html(self):
        request = HttpRequest()
        response = control_panel(request)
        expected_html = render_to_string('control_panel.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)


    def test_new_world_generated_from_POST_request(self):
        x_bounds = [0,50]
        y_bounds = [0,50]
        coords = {x: {y: None for y in range(x_bounds[1])} 
                        for x in range(y_bounds[1])}
        json_coords = json.dumps(coords)        

        self.client.post(
            '/world/new',
        )

        self.assertEqual(World.objects.count(), 1)

        saved_world = World.objects.first()
        saved_world_coords = saved_world.world_coords

        self.assertEqual(json_coords, saved_world_coords)


    # Doesn't seem to work with templates that receive JSON?
    #def test_uses_world_view_template(self):
    #    world = World.objects.create()
    #    response = self.client.get('/world/{}/'.format(world.id))
    #
    #    self.assertTemplateUsed(response, 'control_panel.html')


    def test_passes_correct_world_coords_to_template(self):
        world_coords = WorldGrid().world_coords

        correct_world = World.objects.create(world_coords=world_coords)
        world_coords = None
        if hasattr(correct_world, 'world_coords'):
            world_coords = json.loads(correct_world.world_coords)
        response = self.client.get('/world/{}/'.format(correct_world.id))

        self.assertEqual(response.context['world_coords'], world_coords)


    def test_saving_and_retrieving_blob_coords(self):
        world_coords = WorldGrid().world_coords
        world_ = World.objects.create(world_coords=world_coords)
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


    def test_displays_only_blobs_for_that_world(self):
        world_coords = WorldGrid().world_coords

        correct_world = World.objects.create(world_coords=world_coords)

        Blob.objects.create(x=1, y=2, world=correct_world)
        Blob.objects.create(x=3, y=4, world=correct_world)

        other_world = World.objects.create(world_coords=world_coords)
        Blob.objects.create(x=5, y=6, world=other_world)
        Blob.objects.create(x=7, y=8, world=other_world)

        response = self.client.get('/world/{}/'.format(correct_world.id))

        self.assertEqual(1, response.context['blobs'][0].x)
        self.assertEqual(2, response.context['blobs'][0].y)
        self.assertEqual(3, response.context['blobs'][1].x)
        self.assertEqual(4, response.context['blobs'][1].y)
        for blob in response.context['blobs']:
            self.assertNotEqual(5, blob.x)
            self.assertNotEqual(6, blob.y)
            self.assertNotEqual(7, blob.x)
            self.assertNotEqual(8, blob.y)



class NewWorldTest(TestCase):

    def test_uses_grid_template(self):
        world = World.objects.create()
        response = self.client.get('/grid/new'.format(world.id))
        self.assertTemplateUsed(response, 'grid.html')


    def test_saving_a_new_world_creation_from_POST_request(self):
        x_bounds = [0,50]
        y_bounds = [0,50]
        coords = {x: {y: None for y in range(x_bounds[1])} 
                        for x in range(y_bounds[1])}
        json_coords = json.dumps(coords)        

        self.client.post(
            '/grid/new',
        )

        self.assertEqual(World.objects.count(), 1)

        saved_world = World.objects.first()
        saved_world_coords = saved_world.world_coords
        self.assertEqual(json_coords, saved_world_coords)


    def test_saving_and_retrieving_worlds(self):
        world_1 = World()
        world_1.world_coords = json.dumps(WorldGrid().world_coords)
        world_1.save()

        world_2 = World()
        world_2.world_coords = json.dumps(WorldGrid().world_coords)
        world_2.save()

        x_bounds = [0,50]
        y_bounds = [0,50]
        coords = {x: {y: None for y in range(x_bounds[1])} 
                        for x in range(y_bounds[1])}
        json_coords = json.dumps(coords)        

        saved_worlds = World.objects.all()
        self.assertEqual(saved_worlds.count(), 2)

        first_saved_world = saved_worlds[0]
        second_saved_world = saved_worlds[1]
        self.assertEqual(json_coords, json.loads(first_saved_world.world_coords))
        self.assertEqual(json_coords, json.loads(second_saved_world.world_coords))
        




class AddBlobTest(TestCase):
    pass