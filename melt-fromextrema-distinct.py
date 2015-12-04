#!/usr/bin/python

from PIL import Image
from math import cos, pi
import sys
import random
import heapq
import itertools

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

infile = sys.argv[1]
im = Image.open(infile).convert("RGB")
#im.thumbnail((600,600)) # make sure dimensions are sane
h = im.size[1]

extrema = []
for x in range(0, im.size[0]):
    if x%10==0: print(x, end=" ")
    sys.stdout.flush()

    local = []
    for y in range(0, im.size[1]):
        pix = im.getpixel((x, y))
        pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2
        heapq.heappush(local, (-pixweight, (x, y)))

    local.sort()
    i = 0
    while i < len(local):
        local = [pix for pix in local if abs(pix[1][1] - local[i][1][1]) > 5]
        i += 1

    extrema += heapq.nsmallest(8, local)

# first we clip off the least remarkable 10th of the extrema
# then, we order the remaining ones by y-coordinate
extrema = sorted(extrema)[:-(len(extrema)//10)]
extrema.sort(key=lambda t:t[1][1])
print("\n", len(extrema), "extrema collected and ordered!")
print(" Sorting...")

y2_old = 0
for weight, extremum in extrema:
    #print(".", end="")
    #sys.stdout.flush()
    x = extremum[0]
    y2 = extremum[1]
    y1 = max(y2 - random.randint(1, h//3), 0)

    #y1 = extremum[1]
    #y2 = min(y1 + random.randint(1, h//34)**2, h)

    for _, point in extrema:
        if point[1] >= y2: continue
        if point[1] > y1: y1 = point[1]

    pixels = []
    for y in range(y1, y2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)

    for i, y in enumerate(range(y1, y2)):
        im.putpixel((x, y), pixels[i])
    y2_old = y2


outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
