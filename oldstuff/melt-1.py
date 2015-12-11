#!/usr/bin/python

from PIL import Image
import sys
import random
from math import cos, pi

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

infile = sys.argv[1]
im = Image.open(infile).convert("RGB")
im.thumbnail((512,512)) # make sure dimensions are sane

for x in range(0, im.size[0]):
    weight = int(im.size[1]*(2+cos(x*2*pi/im.size[0]))/4)
    weight += random.randint(-im.size[0], im.size[0]) // 16
    weight = max(weight, 1)
    weight = min(weight, im.size[1])

    pixels = []
    for y in range(im.size[1] - weight, im.size[1]):
        pixels.append(im.getpixel((x, y)))

    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=True)

    for i, y in enumerate(range(im.size[1] - weight, im.size[1])):
        im.putpixel((x, y), pixels[i])

outfile = ''.join(infile.split(".")[:-1]) + "_sorted"
im.save(outfile, "PNG")
