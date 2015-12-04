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
im.thumbnail((900,700)) # make sure dimensions are sane
h = im.size[1]

extrema = []
for y in range(0, im.size[1]):
    if y%10==0: print(y, end=" ")
    sys.stdout.flush()

    local = []
    for x in range(0, im.size[0]):
        pix = im.getpixel((x, y))
        pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2
        heapq.heappush(local, (-pixweight, (x, y)))
    extrema += heapq.nsmallest(16, local)

extrema = sorted(extrema)[:-(len(extrema)//10)]
i = 0
print("")
print(len(extrema))
while i < len(extrema):
    x = extrema[i][1][0]
    y = extrema[i][1][1]
    extrema = [point for point in extrema
               if (x-point[1][0])**2 + (y-point[1][1])**2 > 3]
    i += 1
print(len(extrema))

print("\n", len(extrema), "extrema collected, ordered, and filtered!")
print(" Sorting...")

for weight, extremum in extrema:
    x = extremum[0]
    y2 = extremum[1]
    y1 = max(y2 - random.randint(1, h//3), 0)
    #y1 = extremum[1]
    #y2 = min(y1 + random.randint(1, h//34)**2, h)

    pixels = []
    for y in range(y1, y2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)

    for i, y in enumerate(range(y1, y2)):
        im.putpixel((x, y), pixels[i])


outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
