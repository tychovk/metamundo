from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.generator import WorldGrid, BlobManager
from app.views import home_page
from app.views import control_panel


import logging
import math

logging.basicConfig(level=logging.INFO)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


    def test_world_grid_is_correct_size(self):
        world_grid = WorldGrid()

        self.assertEqual(len(world_grid.coords), 500)
        self.assertEqual(len(world_grid.coords[0]), 500)


    def num_blobs_spawner(self, num_tries=1):
        world_grid = WorldGrid()
        blob_manager = BlobManager(world_grid)
        for try_spawn in range(num_tries):
            spawn_attempt = blob_manager.spawn_blob(world_grid)

        return blob_manager

    def test_blob_spawner_first_blob_gets_saved(self):
        blob_dict = self.num_blobs_spawner(num_tries=1).blob_dict
        num_blobs_spawned = len(blob_dict)
        self.assertEqual(num_blobs_spawned, 1)


    def test_blob_spawner_multiple_blobs(self):
        """
        There's a _very_ small chance this one won't go through. 
        If so, try again a couple of times.
        It may be broken if it fails continuously.
        """

        blob_dict = self.num_blobs_spawner(num_tries=15).blob_dict
        blobs_saved = len(blob_dict)

        self.assertTrue(blobs_saved > 1)


    def test_distance_between_blobs_more_than_200(self):
        distance_limit = 200

        blob_dict = self.num_blobs_spawner(num_tries=15).blob_dict

        x_1 = blob_dict[1]['coords'][0]
        y_1 = blob_dict[1]['coords'][1]
        x_2 = blob_dict[2]['coords'][0]
        y_2 = blob_dict[2]['coords'][1]

        distance = math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

        self.assertTrue(distance > distance_limit)




    def adjust_coords_build(self):
        pass


class ControlPanelTest(TestCase):

    def test_control_panel_url_resolves(self):
        found = resolve('/control_panel')
        self.assertEqual(found.func, control_panel)