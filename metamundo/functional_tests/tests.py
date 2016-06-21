#!usr/bin/env python3
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException

import math



class MetamundoControler(StaticLiveServerTestCase):



    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True


    def test_control_functions(self):

        # A visitor gets to the main page:
        self.browser.get("http://localhost:8000")

        # We see it in the title
        # self.assertIn('Metamundo Control Panel', self.browser.title)

        # There is no grid yet
        self.assertFalse(self.is_element_present(By.ID, "world_grid"))

        # There is an explanation of the website with a "start_world" button
        # We push a button to start the world
        start_world_box = self.browser.find_element_by_id('start_world')
        start_world_box.send_keys(Keys.ENTER)

        # Now the page contains a grid
        self.assertTrue(self.is_element_present(By.ID, "world_grid"))
        first_world = self.browser.current_url

        # Oops, we accidentally pressed the button twice
        start_world_box = self.browser.find_element_by_id('start_world')
        start_world_box.send_keys(Keys.ENTER)

        # A pop-up message appears, asking if we really want to create a new
        # world.



        # Now the page contains a grid again
        self.assertTrue(self.is_element_present(By.ID, "world_grid"))
        second_world = self.browser.current_url

        # The first world we created is not the same as the second one
        self.assertNotEqual(first_world, second_world)

        # After we've created/selected a world, we see three new buttons:
        # - Spawn blob (with text box for choosing coords)
        self.assertTrue(self.is_element_present(By.ID, "spawn_blob"))
        self.assertTrue(self.is_element_present(By.ID, "new_blob_coords"))
        
        # - Start simulation
        self.assertTrue(self.is_element_present(By.ID, "start_simulation"))

        # - Add blob (different colour, which stays activated until esc or the
        #   right-mouse button is clicked) to click-add blobs
        self.assertTrue(self.is_element_present(By.ID, "add_blob_at"))

        ## Spawn Blob
        # We press the "Spawn Blob" button...
        spawn_blob_box = self.browser.find_element_by_id("spawn_blob")
        spawn_blob_box.send_keys(Keys.ENTER)

        # A status box shows tells us where the blob was placed.
        status_box = self.browser.find_element_by_id("status_box")
        self.assertIn("New blob was spawned at:", status_box.text)
        new_blob_coords = [int(s) for s in re.findall(r'[-+]?\d+', status_box)]
        self.assertTrue(len(new_blob_coords), 2)

        # We see that box in the grid now green


        # If no (random) blob could be spawned (due to rules), a message 
        # makes clear that it can't happen.


        # There's a dropdown menu too where we can select an already existing
        # world...
        self.assertTrue(self.is_element_present(By.ID, "select_world"))
        
        #  We click & select the first world we created.
        select_world = self.browser.find_element_by_id('select_world_1')
        select_world.click()
        

        
        

        self.fail('Finish writing tests!')

        # It has a button in the midde of the grid that reads 
        #   "And so it begins..."


        # Clicking anywhere on the grid makes the message go away


        # And a first blob is spawned.


        # There now is another button below the grid that reads 
        #   "Spawn another blob"



        


        # The user sees a grid of 500 by 500. 
        grid = self.browser.find_element_by_id('world_grid')
        

        # .. and also sees a button that says "Spawn Solitary Blob on a 
        # random spot", when it's pushed, the user sees a blob spawn on a 
        # random spot on the map.
        
        # There is another button that reads "Evolve Blobs".
        # This button is clicked, and all blob-units evolve in a random 
        # direction.

        # The user can also sees a "Let there be time" a button that starts
        # the time and simulates the previously mentioned steps. 
        
        # The button is replaced with a button that says "Stop the time".
        # This button is clicked, and the time is stopped.




"""
class MetamundoTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_world(self):

        # We go to our live homepage:
        self.browser.get("http://localhost:8000")

        # There is a 2D world that is organized in a rectangular grid with
        # coordinates. The world starts as a grid that is 500 x 500.

        self.assertEqual(len(world_grid.coords), 500)
        self.assertEqual(len(world_grid.coords[0]), 500)

        # In the beginning of the game, one blob is already spawned
        blob_manager = BlobManager(world_grid)
        blob_manager.spawn_blob(world_grid)
        num_blobs = len(blob_manager.blob_dict)
        self.assertNotEqual(num_blobs, 0)

        # on a random spot on the grid...
        blob_coords_list = [blob_manager.blob_dict[blob]['coords'] for \
                            blob in blob_manager.blob_dict]
        
        for blob_coords in blob_coords_list:
            self.assertIn(blob_coords[0], world_grid.coords)
            self.assertIn(blob_coords[1], world_grid.coords[0])

        # A spot that is at least 200 steps away from another blob.
        # Let's spawn a second one. It's possible that the blob that would be 
        # spawned is too close to other blobs (within 200 steps), in that case:
        # - the console is logged
        # - a message is returned dictating that
        new_blob_result = blob_manager.spawn_blob(world_grid)
        function_worked = None

        if new_blob_result == 'New blob would be too close to old blobs. ' \
                                'No new blob today!':
            function_worked = True

        elif len(blob_manager.blob_dict) == 2:
            coords_1 = blob_manager.blob_dict[1]['coords']
            coords_2 = blob_manager.blob_dict[2]['coords']

            distance = math.sqrt((coords_1[0] - coords_2[0])**2 +
                                 (coords_1[1] - coords_2[1])**2)

            print (distance)                           # TO BE REMOVED LATER
            print (coords_1, coords_2)                 # TO BE REMOVED LATER


            if distance >= 200:
                function_worked = True


        self.assertTrue(function_worked)

        # When we actually start the game,
        # periodically new blobs spawn following the rules above. Let's reset.
        blob_manager = BlobManager(world_grid)
        # We're at day 0
        init_day = blob_manager.day
        self.assertEqual(init_day, 0)

        blob_manager.start(world_grid)
        # There should be one blob now:
        num_blobs = len(blob_manager.blob_dict)
        self.assertEqual(num_blobs, 1)

        # And we're at day 1:
        start_day = blob_manager.day
        self.assertEqual(start_day, 1)



        # Every 2 minutes, in a spot adjacent to a B spot, a Blob (B) can spawn 
        # ..unless:
        # - That spot is occupied
        #       No double Blobbing
        # - There is a B in a 1 step radius with a birthday difference > 10 with the B
        #       Blobs have too much respect for their elderly to procreate next to them
        # - The B has an age of < 12 or > 15
        #       Young blobs don't procreate. 
        #       Blobs have a small window of procreation. The internal clock is real!

        # A player can spawn randomly within 25 steps of a blob 
        # Players cannot step on blobs unless:
        # - The blobs have an age < 4 (the blob will be destroyed this way)
        # - The blob has an  4 < age < 10 (the player stands in the blob)

        # Diego is a player.
        diego = Player(world_grid = world_grid, name = 'Diego')

        # Diego is on the world. 
        x = diego.x
        y = diego.y
        self.assertIn(y, world_grid.coords[x])



        # Just like any player, he is shown the area around him 12 steps 
        # in all directions.
        
        
        # Players can walk through the area in up, down, left, right
        ### But they can also move also diagonally.
        self.fail('So far, so good.')


        # Blob characteristics:
        # To be determined
"""