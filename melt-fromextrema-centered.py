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
im = Image.open(infile)
im.convert("RGB")
im.thumbnail((700,700)) # make sure dimensions are sane
h = im.size[1]

extrema_top = []
extrema_bottom = []
for x in range(0, im.size[0]):
    if x%10==0: print(x, end=" ")
    sys.stdout.flush()
    #max_top = (float("inf"), (0, 0))
    #max_bottom = (float("inf"), (0, 0))
    max_top = (0, (0, 0))
    max_bottom = (0, (0, 0))

    for y in range(0, im.size[1]):
        pix = im.getpixel((x, y))
        pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2

        if y <= h//2:
            if pixweight > max_top[0]:
                max_top = (pixweight, (x, y))
        else:
            if pixweight > max_bottom[0]:
                max_bottom = (pixweight, (x, y))

    extrema_top.append(max_top)
    extrema_bottom.append(max_bottom)

extrema_top = sorted(extrema_top, reverse=True)[:-200]
extrema_bottom = sorted(extrema_bottom, reverse=True)[:-200]
print("\nExtrema collected and sorted!")

for weight, extremum in itertools.chain(extrema_top, extrema_bottom):
    print(".", end="")
    sys.stdout.flush()
    x = extremum[0]
    y1 = extremum[1]

    pixels = []
    if y1 <= h//2:
        for y2 in range(y1, h//2):
            pixels.append(im.getpixel((x, y2)))
        pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=True)
        for i, y2 in enumerate(range(y1, h//2)):
            im.putpixel((x, y2), pixels[i])
    else:
        for y2 in range(h//2, y1):
            pixels.append(im.getpixel((x, y2)))
        pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)
        for i, y2 in enumerate(range(h//2, y1)):
            im.putpixel((x, y2), pixels[i])


outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
print(im.size[1])
