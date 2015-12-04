#!/usr/bin/python

# so named because it creates beautiful abstract art

from PIL import Image
import sys
import random
import itertools
import collections

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

infile = sys.argv[1]
im = Image.open(infile).convert("RGB")
im.thumbnail((900,700)) # make sure dimensions are sane
w = im.size[0]
h = im.size[1]

grid = [[None]*h for i in range(w)]
points = []
for i in range(20):
    points.append((random.randint(0, w-1),
                   random.randint(0, h-1)))

queues = [collections.deque([point]) for point in points]
weight = 255//len(points)

print("Divvying up the image.")
# loop for as long as we have at least one nonempty queue
while False in [len(queue) == 0 for queue in queues]:
    for i in range(len(queues)):
        try:
            point = queues[i].popleft()
            while grid[point[0]][point[1]] is not None:
                point = queues[i].popleft()

        except IndexError:
            # queue empty
            continue

        grid[point[0]][point[1]] = i

        # enqueue neighbors
        for delta in ((1, 0), (0, -1), (-1, 0), (0, 1)):
            x_ = point[0]+delta[0]
            y_ = point[1]+delta[1]
            if x_ < 0 or x_ >= w: continue
            if y_ < 0 or y_ >= h: continue
            if grid[x_][y_] is not None: continue
            queues[i].append((x_, y_))

assert True not in [None in col for col in grid]

for x in range(w):
    for y in range(h):
        im.putpixel((x, y,), (weight*grid[x][y],)*3)

outfile = ''.join(infile.split(".")[:-1]) + "_ignored.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
