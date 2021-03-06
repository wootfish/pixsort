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

#def metric(pix):
#    return pix[0]**2 - pix[1]**2 - pix[2]**2

extrema = []
for x in range(0, im.size[0]):
    if x%10==0: print(x, end=" ")
    sys.stdout.flush()

    local = []
    for y in range(0, im.size[1]):
        pix = im.getpixel((x, y))
        pixweight = pix[0]**2 - (pix[1]**2 + pix[2]**2)/2 #metric(pix)
        heapq.heappush(local, (-pixweight, (x, y)))
    extrema += heapq.nsmallest(10, local)

extrema = sorted(extrema)[:-(len(extrema)//8)]
print("\n", len(extrema), "extrema collected and ordered!")
print(" Sorting...")

for weight, extremum in extrema:
    #print(".", end="")
    #sys.stdout.flush()
    x = extremum[0]
    #y2 = extremum[1]
    #y1 = max(y2 - random.randint(1, h//3), 0)
    y1 = extremum[1]
    y2 = min(y1 + random.randint(1, h//34)**2, h)

    pixels = []
    for y in range(y1, y2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda p : p[0]**2 + p[1]**2 + p[2]**2, reverse=False)

    for i, y in enumerate(range(y1, y2)):
        im.putpixel((x, y), pixels[i])


outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
