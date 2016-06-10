#!usr/bin/env python3
import unittest
from app.generator import WorldGrid, BlobManager, Player
import math


class MetamundoTest(unittest.TestCase):
    def test_world(self):
        # There is a 2D world that is organized in a rectangular grid with
        # coordinates. The world starts as a grid that is 1200 x 1200.
        world_grid = WorldGrid()

        self.assertEqual(len(world_grid.coords), 1200)
        self.assertEqual(len(world_grid.coords[0]), 1200)

        # When the game starts, one blob is already spawned
        blob_manager = BlobManager(world_grid)
        blob_manager.start(world_grid)
        num_blobs = len(blob_manager.blob_dict)
        self.assertNotEqual(num_blobs, 0)

        # on a random spot on the grid...
        blob_coords_list = [blob_manager.blob_dict[blob]['coords'] for \
                            blob in blob_manager.blob_dict]
        
        for blob_coords in blob_coords_list:
            self.assertIn(blob_coords[0], world_grid.coords)
            self.assertIn(blob_coords[1], world_grid.coords[0])

        # A spot that is at least 600 steps away from another blob.
        # Let's spawn a second one. It's possible that the blob that would be 
        # spawned is too close to other blobs (within 600 steps), in that case:
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

            if distance >= 600:
                function_worked = True

        self.assertTrue(function_worked)




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

if __name__ == '__main__':
    unittest.main()