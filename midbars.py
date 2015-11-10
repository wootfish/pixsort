#!/usr/bin/python

from PIL import Image
import sys
import random
from math import cos, pi

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

def hypot(pix):
    return sum(map(lambda x:x**2, pix))

infile = sys.argv[1]
im = Image.open(infile)
im.thumbnail((600,600)) # make sure dimensions are sane

print("Image width:", im.size[0])
print("Processing...", end="")

w = im.size[0]
h = im.size[1]
for x in range(0, w):
    if x%10 == 0:
        print(x, " ", end="")
        sys.stdout.flush()

    #y1 = int(random.gauss(h//2, h//4))
    y1 = int(h/2 - abs(random.gauss(h//5, h//10)))
    if y1 < 0: y1 = 0
    if y1 > h-2: y1 = h-2

    y2 = int((h//2) - (y1 - h//2))

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

print("")

outfile = ''.join(infile.split(".")[:-1]) + "_sorted"
im.save(outfile, "PNG")
