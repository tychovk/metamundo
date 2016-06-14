from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.generator import WorldGrid
from app.views import home_page
from app.views import control_panel
from app.models import World


import logging
import math
import json

logging.basicConfig(level=logging.INFO)


class ControlPanelTest(TestCase):

    def test_control_panel_url_resolves(self):
        found = resolve('/control_panel')
        self.assertEqual(found.func, control_panel)


    def test_control_panel_returns_correct_html(self):
        request = HttpRequest()
        response = control_panel(request)
        expected_html = render_to_string('control_panel.html')
        self.assertEqual(response.content.decode(), expected_html)



class NewWorldTest(TestCase):

    def test_uses_grid_template(self):
        world = World.objects.create()
        response = self.client.get('/grid/new'.format(world.id))
        self.assertTemplateUsed(response, 'grid.html')


    def test_saving_a_new_world_creation_from_POST_request(self):
        x_bounds = [0,500]
        y_bounds = [0,500]
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

        x_bounds = [1,500]
        y_bounds = [1,500]
        coords = {x: {y: None for y in range(x_bounds[1])} 
                        for x in range(y_bounds[1])}
        json_coords = json.dumps(coords)        

        saved_worlds = World.objects.all()
        self.assertEqual(saved_worlds.count(), 2)

        first_saved_world = saved_worlds[0]
        second_saved_world = saved_worlds[1]
        self.assertEqual(json_coords, first_saved_world.world_coords)
        self.assertEqual(json_coords, second_saved_world.world_coords)
        




class AddBlobTest(TestCase):
    pass

