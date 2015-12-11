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

extrema = []
for x in range(0, im.size[0]):
    if x%10==0: print(x, end=" ")
    sys.stdout.flush()
    heap = []
    for y in range(0, im.size[1]):
        pix = im.getpixel((x, y))
        pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2 
        heapq.heappush(heap, (-pixweight, (x, y)))

    heap = heapq.nsmallest(1, heap)
    extrema += heap

extrema = sorted(extrema)[:-200]
print("\nExtrema collected and sorted!")

h = im.size[1]

for weight, extremum in extrema:
    print(".", end="")
    sys.stdout.flush()
    #height = random.randint(im.size[1]//17, im.size[1]//8)
    #height = int(abs(random.gauss(im.size[1]//34, im.size[1]//85))*im.size[1]//34)
    #height = 100
    x = extremum[0]
    y = extremum[1]
    #y2 = min(im.size[1], y1+height)

    if y2 <= im.size[1]//2 or y1 >= im.size[1]//2:
        pixels = []
        for y in range(y1, y2):
            pixels.append(im.getpixel((x, y)))
        pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=(y2 <= im.size[1]//2))
        for i, y in enumerate(range(y1, y2)):
            im.putpixel((x, y), pixels[i])
    else:
        pixels = []
        for y in range(y1, h//2):
            pixels.append(im.getpixel((x, y)))
        pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=True)
        for i, y in enumerate(range(y1, h//2)):
            im.putpixel((x, y), pixels[i])

        pixels = []
        for y in range(h//2, y2):
            pixels.append(im.getpixel((x, y)))
        pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)
        for i, y in enumerate(range(h//2, y2)):
            im.putpixel((x, y), pixels[i])


outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")

print("\nFile saved:", outfile)
print(im.size[1])
