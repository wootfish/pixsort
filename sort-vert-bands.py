#!/usr/bin/python

# todo: make this not be dumb

from PIL import Image
import sys
import random
import itertools
import kdtree

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

for i in range(200):
    if random.random() < 0.00:
        x1 = random.randint(0, w-1)
        x2 = random.randint(0, w-1)
        y = random.randint(0, h-1)

        if x1 > x2: x1, x2 = x2, x1
        sort_row(im, x1, x2, y)
    else:
        y1 = random.randint(0, h-1)
        y2 = random.randint(0, h-1)
        x = random.randint(0, w-1)

        if y1 > y2: y1, y2 = y2, y1
        sort_col(im, x, y1, y2)

#regionctrs = []
#pointsets = {}
#for i in range(20):
#    point = (random.randint(0, w-1), random.randint(0, h-1))
#    regionctrs.append(point)
#    pointsets[point] = set()
#
#tree = kdtree.create(regionctrs)
#
#for y in range(w):
#    if x%10==0: print(x)
#    for x in range(h):
#        nearest = tree.search_nn((x, y))[0].data
#        pointsets[nearest].add((x, y))
#
#for key in pointsets:
#    cols = [[]]
#    prev = None
#    for point in sorted(pointsets[key]):
#        if prev is not None and point[0] != prev[0]:
#            cols.append([])
#
#        pweight = point[0]**2 + point[1]**2 + point[2]**2
#        cols[-1].append((pweight, point))
#
#    for col in cols:
#        col.sort()



outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
