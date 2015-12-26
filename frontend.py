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

        self.region2 = tk.Frame(
            frame,
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
        self.currsort.set(sorted(self.sorts)[0])
        self.currsort.trace("w", self.update_controls)

        self.sortpicker = tk.OptionMenu(
            self.region2,
            self.currsort,
            *sorted(self.sorts),
        )

        # slider for adjusting number of rounds
        self.roundslider = tk.Scale(
            self.region3,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
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
        self.region1.grid(row=0, column=0, rowspan=9, columnspan=3)
        self.imglabel.grid(column=0, row=0, columnspan=3)
        self.undobutton.grid(column=0, row=1)
        self.indexlabel.grid(column=1, row=1)
        self.redobutton.grid(column=2, row=1)

        self.region2.grid(row=0, column=3)
        self.sortpicker.grid(column=3, row=0, columnspan=2)

        self.region3.grid(row=3, column=3, rowspan=3, columnspan=2)
        self.progress1.grid(column=3, row=1, columnspan=2)

        self.region4.grid(row=8, column=3)
        self.drawbutton.grid(column=3, row=0)
        self.savebutton.grid(column=4, row=0)

        # now take care of sort-specific widgets
        self.update_controls()

    def update_controls(self, *args):
        print("Update event triggered.")
        print(args)
        print(self.currsort.get())

        # remove every sort-specific widget, then add back the ones we want
        self.roundslider.grid_remove()
        self.progress2.grid_remove()

        sort = self.sorts[self.currsort.get()]

        if sort == self.sort_pairs:
            print("sort_pairs")
            self.roundslider.grid(column=3, row=0, columnspan=2)

        elif sort == self.sort_lines:
            print("sort_lines")
            self.roundslider.grid(column=3, row=0, columnspan=2)

        elif sort == self.sort_extrema:
            print("sort_extrema")
            self.progress2.grid(column=3, row=2, columnspan=2)

        else:
            print("sort identification logic broke")

    def save_img(self):
        parts = sys.argv[1].split(".")
        name = ''.join(parts[:-1]) + "_" + time.strftime("%Y-%m-%d_%I:%M:%S")
        ext = parts[-1]

        filename = name + "." + ext
        self.images[self.img_index].save(filename, "PNG")

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
        self.sort_pairs_internal(im, rounds=self.roundslider.get())

    def sort_lines(self, im):
        self.sort_lines_internal(im, rounds=self.roundslider.get())

    def sort_extrema(self, im):
        self.sort_extrema_internal(im, minima=False, reverse=False)

    def sort_pairs_internal(self, im, rounds=30, vert=False):
        self.progress1.configure(maximum=rounds, value=0)
        for i in range(rounds):
            for _ in range(5*max(im.size)):
                x = random.randrange(0, im.size[0] - (1 if vert else 2))
                y = random.randrange(0, im.size[1] - (2 if vert else 1))
                p1 = (x, y)
                p2 = (x, y+1) if vert else (x+1, y)

                while weight(im.getpixel(p1)) >= weight(im.getpixel(p2)):
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

    def sort_extrema_internal(self, im, percol=5, reverse=True, minima=True, mindist=5,
                    trimfactor=2):

        self.progress1.configure(maximum=im.size[0]+1, value=0, mode="determinate")
        self.progress2.configure(value=0)
        extrema = []

        # loop over columns, collecting top maximums or minimums of each
        # after this loop we have a populated extrema list & can start sorting
        for x in range(0, im.size[0]):
            local = []
            for y in range(0, im.size[1]):
                pix = im.getpixel((x, y))
                pixweight = pix[0]**2 + pix[1]**2 + pix[2]**2
                local.append((pixweight*(1 if minima else -1), (x, y)))
            local.sort()

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
            extrema.sort()
            extrema = extrema[:-len(extrema)//trimfactor]

        self.progress2.configure(maximum=len(extrema))
        drawcounter = 0
        for _, extremum in extrema:
            drawcounter += 1
            x = extremum[0]
            y = extremum[1]
            yprime = max(y - random.randint(1, im.size[1]//3), 0)

            pixels = []
            for y in range(yprime, y):
                pixels.append(im.getpixel((x, y)))
            pixels.sort(key=weight, reverse=reverse)

            for j, y in enumerate(range(yprime, y)):
                im.putpixel((x, y), pixels[j])

            self.progress2.step()
            if drawcounter % 40 == 0:
                self.redraw()
                drawcounter = 0

        self.progress1.step()


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
