#!/usr/bin/python

from PIL import Image
import sys
import random
from math import sin, cos, pi

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" filename.png")
    exit(1)

def hypot(pix):
    return sum(map(lambda x:x**2, pix))

infile = sys.argv[1]
im = Image.open(infile)
im = im.convert("RGB")
im.thumbnail((700,700)) # make sure dimensions are sane

print("Image width:", im.size[0])
print("Processing...", end="")

w = im.size[0]
h = im.size[1]
for x in range(0, w):
    if x%10 == 0:
        print(x, " ", end="")
        sys.stdout.flush()

    #y1 = int(random.gauss(h//2, h//4))
    #y1 = int(h/2 - 0.7*abs(0.7*random.gauss(h//17, h//6) + (h/9)*(1+cos(2*pi*x/w))))
    y1 = int(h/2 - random.random()**1.6 *(h/8)*(2.2+cos(2*pi*x/w)))
    if y1 < 2: y1 = 2
    if y1 > h-2: y1 = h-2

    y2 = int((h//2) - (y1 - h//2))

    #y1 = max(y1-h//7, 0)
    #y2 = max(y2-h//7, 0)

    pixels = []
    for y in range(y1, (y1+y2)//2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)

    for i, y in enumerate(range(y1, (y1+y2)//2)):
        im.putpixel((x, y), pixels[i])

    pixels = []
    for y in range((y1+y2)//2, y2):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=True)

    for i, y in enumerate(range((y1+y2)//2, y2)):
        im.putpixel((x, y), pixels[i])

    pixels = []
    for y in range((3*y1+2*y2)//5, (2*y1+3*y2)//5):
        pixels.append(im.getpixel((x, y)))
    pixels.sort(key=lambda pixel : pixel[0]**2 + pixel[1]**2 + pixel[2]**2, reverse=False)

    for i in range(len(pixels)):
        offset = (i+1)//2 * ((-1)**(i%2))
        im.putpixel((x, (y1+y2)//2+offset), pixels[i])

print("")

outfile = ''.join(infile.split(".")[:-1]) + "_sorted.png"
im.save(outfile, "PNG")
