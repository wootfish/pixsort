#!/usr/bin/python

# todo: make this not be dumb

from PIL import Image
import sys
import random
import itertools
import kdtree
import collections

def sort_row(im, x1, x2, y, reverse=True):
    pixels = []
    for x in range(x1, x2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=reverse)

    for i, x in enumerate(range(x1, x2)):
        im.putpixel((x, y), pixels[i])

def sort_col(im, x, y1, y2, reverse=True):
    pixels = []
    for y in range(y1, y2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=reverse)

    for i, y in enumerate(range(y1, y2)):
        im.putpixel((x, y), pixels[i])

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

infile = sys.argv[1]
im = Image.open(infile).convert("RGB")
im.thumbnail((700,700)) # make sure dimensions are sane
w = im.size[0]
h = im.size[1]

grid = [[None]*h for i in range(w)]
points = []
for i in range(20):
    points.append((random.randint(0, w-1),
                   random.randint(0, h-1)))

queues = [collections.deque([point]) for point in points]

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

print("Sorting pixels.")
for x in range(w):
    if x%10==0:
        print(x, end=" ")
        sys.stdout.flush()
    for y in range(h):
        # we mark pixels as sorted by setting their grid value to -1
        # skip pixels that've already been sorted
        if grid[x][y] < 0:
            continue

        i = grid[x][y]
        x_ = x
        while x_ < w and grid[x_][y] == i:
            grid[x_][y] = -1   # mark cell as sorted
            x_ += 1
        sort_row(im, x, x_, y)

#colors = []
#for i in range(len(points)):
#    r, g, b, n = 0, 0, 0, 0
#    for point in [(x, y) for x in range(w) for y in range(h) if grid[x][y]==i]:
#        n += 1
#        pix = im.getpixel(point)
#        r += pix[0]
#        g += pix[1]
#        b += pix[2]
#    r //= n
#    g //= n
#    b //= n
#    colors.append((r, g, b))
#
#for x in range(w):
#    for y in range(h):
#        im.putpixel((x, y), colors[grid[x][y]])

outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
