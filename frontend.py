#!/usr/bin/python3

# http://effbot.org/tkinterbook/tkinter-hello-again.htm

import time
import sys
import random
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master, im):
        frame = tk.Frame(master)
        frame.grid()
        self.frame = frame

        # decoration frames
        self.region1 = tk.Frame(
            frame,
            relief=tk.RAISED,
            bd=2,
        )

        self.region2 = tk.LabelFrame(
            frame,
            text="Sort Method",
            labelanchor="n",
            relief=tk.RAISED,
            bd=2,
        )

        self.region3 = tk.Frame(
            frame,
            relief=tk.SUNKEN,
            bd=2,
        )

        self.region4 = tk.Frame(
            frame,
            relief=tk.RAISED,
            bd=2,
        )

        # picture
        self.images = [im]
        self.img_index = 0
        self.photo = ImageTk.PhotoImage(self.images[self.img_index])
        self.imglabel = tk.Label(self.region1, image=self.photo)

        # undo/redo system
        self.undobutton = tk.Button(
            self.region1,
            text="Prev",
            command=self.decrement_ind,
        )

        self.redobutton = tk.Button(
            self.region1,
            text="Next",
            command=self.increment_ind,
        )

        self.indexlabel = tk.Label(
            self.region1,
            text=str(self.img_index),
        )

        # sort-picker menu & associated stringvar
        self.sorts = {
            "Pixel swap":self.sort_pairs,
            "Band sort":self.sort_lines,
            "Sort from extrema":self.sort_extrema,
        }
        self.currsort = tk.StringVar()
        #self.currsort.set(sorted(self.sorts)[0])
        self.currsort.set("Sort from extrema")
        self.currsort.trace("w", self.update_controls)

        self.sortpicker = tk.OptionMenu(
            self.region2,
            self.currsort,
            *sorted(self.sorts),
        )

        # direction picker for extrema sort
        self.dirboxlabel = tk.Label(
            self.region3,
            text="Pick a sort direction:",
        )
        self.sortdir = tk.StringVar()
        self.sortdir.set("Up")
        self.dirbox = tk.OptionMenu(
            self.region3,
            self.sortdir,
            "Up",
            "Up & Left",
            "Left",
            "Down & Left",
            "Down",
            "Down & Right",
            "Right",
            "Up & Right",
        )

        # minima-maxima checkbox
        self.sortfrommin = tk.IntVar()
        self.mincheckbox = tk.Checkbutton(
            self.region3,
            text="Sort from brightest",
            variable=self.sortfrommin,
        )

        # clip lines checkbox
        self.clipsortbars = tk.IntVar()
        self.clipcheckbox = tk.Checkbutton(
            self.region3,
            anchor="w",
            text="Clip sort bars",
            variable=self.clipsortbars,
        )

        # trim factor for extrema sort
        # 0 = no trim
        self.trimslider = tk.Scale(
            self.region3,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
        )
        self.trimlabel = tk.Label(
            self.region3,
            text="% of extrema to discard:",
        )

        # extrema per column for extrema sort
        self.percolslider = tk.Scale(
            self.region3,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
        )
        self.percollabel = tk.Label(
            self.region3,
            text="Extrema per column:",
        )

        # invert sort checkbox
        self.invert = tk.IntVar()
        self.invcheckbox = tk.Checkbutton(
            self.region3,
            text="Invert sort order",
            variable=self.invert
        )

        # slider & label for adjusting number of rounds
        self.roundslider = tk.Scale(
            self.region3,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
        )
        self.roundlabel = tk.Label(
            self.region3,
            text="Specify number of iterations:",
        )

        # progress bars (most sorts use one; extrema sort uses two)
        self.progress1 = ttk.Progressbar(
            self.region4,
            orient=tk.HORIZONTAL,
        )

        self.progress2 = ttk.Progressbar(
            self.region4,
            orient=tk.HORIZONTAL,
        )

        # do-interesting-shit button
        self.drawbutton = tk.Button(
            self.region4,
            text="Run!",
            command=self.draw,
        )

        # save button
        self.savebutton = tk.Button(
            self.region4,
            text="Save",
            command=self.save_img,
        )

        # pack all the non-sort-specific widgets into a nice grid layout
        # region1: image
        self.region1.grid(row=0, column=0, rowspan=9, columnspan=3)
        self.imglabel.grid(column=0, row=0, columnspan=3)
        self.undobutton.grid(column=0, row=1)
        self.indexlabel.grid(column=1, row=1)
        self.redobutton.grid(column=2, row=1)

        # region2: sort picker
        self.region2.grid(row=0, column=3, columnspan=3)
        self.sortpicker.grid(column=3, row=0, columnspan=3)

        # region3: custom twiddlers
        self.region3.grid(row=2, column=3, rowspan=5, columnspan=3)
        self.invcheckbox.grid(row=10, column=0, sticky=tk.W)

        # region4: run/save
        self.region4.grid(row=8, column=3, columnspan=3)
        self.drawbutton.grid(column=0, row=0)
        self.savebutton.grid(column=1, row=0)
        self.progress1.grid(column=0, row=1, columnspan=2)

        # now take care of sort-specific widgets
        self.update_controls()

    def update_controls(self, *args):
        # remove every sort-specific widget, then add back the ones we want
        self.roundslider.grid_remove()
        self.roundlabel.grid_remove()
        self.progress2.grid_remove()
        self.dirbox.grid_remove()
        self.dirboxlabel.grid_remove()
        self.mincheckbox.grid_remove()
        self.clipcheckbox.grid_remove()
        self.trimlabel.grid_remove()
        self.trimslider.grid_remove()
        self.percollabel.grid_remove()
        self.percolslider.grid_remove()

        sort = self.sorts[self.currsort.get()]

        if sort == self.sort_pairs:
            self.roundlabel.grid(column=0, row=0)
            self.roundslider.grid(column=0, row=1, columnspan=2)

        elif sort == self.sort_lines:
            self.roundlabel.grid(column=0, row=0)
            self.roundslider.grid(column=0, row=1, columnspan=2)

        elif sort == self.sort_extrema:
            self.dirboxlabel.grid(column=0, row=0)
            self.dirbox.grid(column=0, row=1)

            self.trimlabel.grid(column=0, row=4)
            self.trimslider.grid(column=0, row=5)
            self.percollabel.grid(column=0, row=6)
            self.percolslider.grid(column=0, row=7)

            self.mincheckbox.grid(column=0, row=8, sticky=tk.W)
            self.clipcheckbox.grid(column=0, row=9, sticky=tk.W)

            self.progress2.grid(column=0, row=2, columnspan=2)

        else:
            print("sort identification logic broke")

    def save_img(self):
        parts = sys.argv[1].split(".")
        name = ''.join(parts[:-1]) + "_" + time.strftime("%Y-%m-%d_%I:%M:%S")

        filename = name + ".png"
        self.images[self.img_index].save(filename, "PNG")
        print("Image saved as", name+".png")

    def decrement_ind(self):
        if self.img_index > 0:
            self.img_index -= 1
        self.redraw()
        self.indexlabel.config(text=str(self.img_index))

    def increment_ind(self):
        if self.img_index < len(self.images)-1:
            self.img_index += 1
        self.redraw()
        self.indexlabel.config(text=str(self.img_index))

    def draw(self):
        self.drawbutton.config(state=tk.DISABLED)
        self.images = self.images[:self.img_index+1]
        self.images.append(self.images[-1].copy())
        self.img_index += 1
        self.indexlabel.config(text=str(self.img_index))
        im = self.images[-1]

        drawfunc = self.sorts[self.currsort.get()]
        #self.sort_pairs_vert(im)
        #self.sort_lines_vert(im)
        drawfunc(im)

        self.drawbutton.config(state=tk.NORMAL)

    def redraw(self):
        self.photo = ImageTk.PhotoImage(self.images[self.img_index])
        self.imglabel.config(image=self.photo)
        self.imglabel.update_idletasks()

    def sort_pairs(self, im):
        self.sort_pairs_internal(
            im,
            rounds=self.roundslider.get(),
            reverse=self.invert.get(),
        )

    def sort_lines(self, im):
        self.sort_lines_internal(
            im,
            rounds=self.roundslider.get(),
            reverse=self.invert.get()
        )

    def sort_extrema(self, im):
        dirpick = self.sortdir.get()
        direction = [0, 0]

        if "Left" in dirpick:
            direction[0] = -1
        elif "Right" in dirpick:
            direction[0] = 1

        if "Up" in dirpick:
            direction[1] = -1
        elif "Down" in dirpick:
            direction[1] = 1

        self.sort_extrema_internal(
            im,
            reverse=self.invert.get(),
            direction=tuple(direction),
            minima=self.sortfrommin.get(),
            clipbars=self.clipsortbars.get(),
            percol=self.percolslider.get(),
            trimfactor=0 if self.trimslider.get() == 0
                       else 100*1/self.trimslider.get(),
        )

    def sort_pairs_internal(self, im, rounds=30, vert=False, reverse=False):
        self.progress1.configure(maximum=rounds, value=0)
        n = -1 if reverse else 1
        for i in range(rounds):
            for _ in range(5*max(im.size)):
                x = random.randrange(0, im.size[0] - (1 if vert else 2))
                y = random.randrange(0, im.size[1] - (2 if vert else 1))
                p1 = (x, y)
                p2 = (x, y+1) if vert else (x+1, y)

                while weight(im.getpixel(p1))*n >= weight(im.getpixel(p2))*n:
                    x = random.randrange(0, im.size[0] - (1 if vert else 2))
                    y = random.randrange(0, im.size[1] - (2 if vert else 1))
                    p1 = (x, y)
                    p2 = (x, y+1) if vert else (x+1, y)

                tmp = im.getpixel(p1)
                im.putpixel(p1, im.getpixel(p2))
                im.putpixel(p2, tmp)
            self.progress1.step()

            if i%3 == 0:
                self.redraw()

    def sort_lines_internal(self, im, rounds=30, reverse=True, vert=True):
        self.progress1.configure(maximum=rounds, value=0)
        for i in range(rounds):
            for _ in range(5):
                x = random.randrange(0, im.size[0]-1)
                y1 = random.randrange(0, im.size[1]-1)
                y2 = random.randrange(0, im.size[1]-1)
                if y1>y2:
                    y1, y2 = y2, y1

                l = []
                for y in range(y1, y2):
                    pix = im.getpixel((x, y))
                    l.append(pix)
                l.sort(key=weight, reverse=reverse)

                for i, y in enumerate(range(y1, y2)):
                    im.putpixel((x, y), l[i])
            self.progress1.step()

            if i%3 == 0:
                self.redraw()

    def sort_extrema_internal(self, im, percol=9, reverse=True, minima=True, mindist=4,
                    trimfactor=8, direction=(1, -1), clipbars=False):

        print(trimfactor)
        self.progress1.configure(maximum=im.size[0]+1, value=0)
        self.progress2.configure(value=0)
        extrema = []

        # builds a list of extrema one column at a time
        for x in range(0, im.size[0]):
            local = []
            for y in range(0, im.size[1]):
                pix = im.getpixel((x, y))
                pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2
                local.append((pixweight, (x, y)))
            local.sort(reverse=minima)

            for i in range(percol):
                if i >= len(local):
                    break
                local = [pix for pix in local if abs(pix[1][1] - local[i][1][1]) > mindist]
            extrema += local[:percol]
            self.progress1.step()

            # redraw is expensive; we use it sparingly in this slow loop
            self.progress1.update_idletasks()

        # trim off the lamest extrema -- negative trimfactor keeps whole list
        if trimfactor > 0:
            extrema.sort(reverse=minima)
            extrema = extrema[:-int(len(extrema)//trimfactor)]

        self.progress2.configure(maximum=len(extrema))
        drawcounter = 0
        absdir = (abs(direction[0]), abs(direction[1]))
        for _, extremum in extrema:
            self.progress2.step()
            x = extremum[0]
            y = extremum[1]

            cap = min(im.size[0]//3,
                      im.size[1]//3,
                      x if direction[0] == -1 else im.size[0]-x-1,
                      y if direction[1] == -1 else im.size[1]-y-1)

            if cap <= 1:
                continue

            delta = random.randint(1, cap)
            xprime = x + delta*direction[0]
            yprime = y + delta*direction[1]

            pixels = []
            startweight = weight(im.getpixel((x, y)))
            x_, y_ = x, y
            while x_ != xprime or y_ != yprime:
                pix = im.getpixel((x_, y_))

                if clipbars and abs(x - x_) > mindist:
                    currweight = weight(pix)
                    # if we started at a local minimum but we've reached
                    # somewhere with an even lower weight, stop
                    if minima and currweight < startweight:
                        break

                    # if we started at a local maximum but we've reached
                    # somewhere with an even greater weight, stop
                    if (not minima) and currweight > startweight:
                        break

                pixels.append(pix)
                x_ += direction[0]
                y_ += direction[1]

            pixels.sort(key=weight, reverse=(reverse^minima))
            for i, pix in enumerate(pixels):
                im.putpixel((x + direction[0]*i, y + direction[1]*i), pix)

            drawcounter += 1
            if drawcounter == 40:
                self.redraw()
                drawcounter = 0

        self.progress1.step()
        self.redraw()


def weight(t):
    r, g, b = t
    return r**2 + g**2 + b**2

def main():
    filename = "prettyshit.png"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    root = tk.Tk()
    im_original = Image.open(filename).convert("RGB")
    im_original.thumbnail((800, 700))

    mainWindow = MainWindow(root, im_original)

    root.mainloop()
    #root.destroy()

if __name__ == "__main__":
    main()
