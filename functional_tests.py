#!usr/bin/env python3
import unittest
from app.app import WorldGrid, Player


class MetamundoTest(unittest.TestCase):
    def test_12_step_radius(self):
        # There is a 2D world that is organized in a rectangular grid with
        # coordinates. The world starts as a grid that is 20 x 20.
        world_grid = WorldGrid()

        # Diego is a player.
        diego = Player(world_grid = world_grid, name = 'Diego')

        # Diego is on the world. Just like any player, he can see the area
        # around him 12 steps in all directions.
        x = diego.x
        y = diego.y
        self.assertIn(y, world_grid.coords[x])
        

        # Players can walk through the area in up, down, left, right
        ### But they can also move also diagonally.
        self.fail('So far, so good.')

        # On the grid, each spot has a 0.5% chance to spawn a Blob (B)..
        # ..unless there is a Blob spot already within a 100 step radius

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







        # Blob characteristics:
        # To be determined

if __name__ == '__main__':
    unittest.main()