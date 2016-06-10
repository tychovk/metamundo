from app import generator

wg = generator.WorldGrid()
bm = generator.BlobManager(wg)

bm.start(wg)