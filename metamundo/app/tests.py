from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.generator import WorldGrid, BlobManager
from app.views import home_page
from app.views import control_panel

import logging

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


    def test_blob_spawner_first_blob(self):
        world_grid = WorldGrid()
        blob_manager = BlobManager(world_grid)
        blob_manager.spawn_blob(world_grid)

        num_blobs_spawned = len(blob_manager.blob_dict)

        self.assertEqual(num_blobs_spawned, 1)
        logging.info("1 Blob-spawn tried, number of blobs should be "
                    "1 and is {}".format(num_blobs_spawned))


    def test_blob_spawner_multiple_blobs(self):
        world_grid = WorldGrid()
        blob_manager = BlobManager(world_grid)

        num_blobs_spawned = 0
        num_tries = 15
        for try_spawn in range(num_tries):
            spawn_attempt = blob_manager.spawn_blob(world_grid)
            if spawn_attempt is True:
                num_blobs_spawned += 1 

        blobs_saved = len(blob_manager.blob_dict)

        self.assertEqual(blobs_saved, num_blobs_spawned)


class ControlPanelTest(TestCase):

    def test_control_panel_url_resolves(self):
        found = resolve('/control_panel')
        self.assertEqual(found.func, control_panel)