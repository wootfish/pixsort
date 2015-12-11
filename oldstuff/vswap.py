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
    if x%10==0:
        print(x, " ", end="")
        sys.stdout.flush()
    numswaps = random.randint(1, int((6*h)**0.5)) ** 2

    for i in range(numswaps):
        #y = random.randint(0, im.size[1]-2)

        y = int(random.gauss(h//2, h//9))
        if y < 0: y = 0
        if y >= h-1: y = h-2

        pix1 = im.getpixel((x, y))
        pix2 = im.getpixel((x, y+1))
        if pix1 < pix2:
            im.putpixel((x, y), pix2)
            im.putpixel((x, y+1), pix1)
print("")

outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")
