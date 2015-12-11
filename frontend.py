#!/usr/bin/python3

# http://effbot.org/tkinterbook/tkinter-hello-again.htm

import time
import sys
import random
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master, im):
        frame = tk.Frame(master)
        frame.grid()
        self.frame = frame

        # picture
        self.images = [im]
        self.img_index = 0
        self.photo = ImageTk.PhotoImage(self.images[self.img_index])
        self.imglabel = tk.Label(frame, image=self.photo)

        # sort-picker menu & associated stringvar
        self.sorts = {
            "Pixel swap":self.sort_pairs,
            "Band sort":self.sort_lines,
        }
        self.currsort = tk.StringVar()
        self.currsort.trace("w", self.update_controls)
        self.currsort.set(sorted(self.sorts)[0])

        self.sortpicker = tk.OptionMenu(
            frame,
            self.currsort,
            *sorted(self.sorts),
        )

        # do-interesting-shit button
        self.drawbutton = tk.Button(
            frame,
            text="Run!",
            command=self.draw,
        )

        # undo/redo system
        self.undobutton = tk.Button(
            frame,
            text="Prev",
            command=self.decrement_ind,
        )

        self.redobutton = tk.Button(
            frame,
            text="Next",
            command=self.increment_ind,
        )

        self.indexlabel = tk.Label(
            frame,
            text=str(self.img_index),
        )

        # save button
        self.savebutton = tk.Button(
            frame,
            text="Save",
            command=self.save_img,
        )

        # pack everything into a nice grid layout
        self.imglabel.grid(column=0, row=0, columnspan=3, rowspan=3)

        self.undobutton.grid(column=0, row=3)
        self.indexlabel.grid(column=1, row=3)
        self.redobutton.grid(column=2, row=3)

        self.sortpicker.grid(column=3, row=0, columnspan=2)
        self.drawbutton.grid(column=3, row=2)
        self.savebutton.grid(column=4, row=2)

    def update_controls(self, *args):
        print("Update event triggered.")
        print(args)
        print(self.currsort.get())

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

    def sort_pairs(self, im, rounds=30, vert=False):
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
            self.redraw()

    def sort_lines(self, im, rounds=30, reverse=True, vert=True):
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
            self.redraw()

def weight(t):
    r, g, b = t
    return r**2 + g**2 + b**2

def main():
    assert len(sys.argv) > 1

    root = tk.Tk()
    im_original = Image.open(sys.argv[1]).convert("RGB")
    im_original.thumbnail((800, 600))

    mainWindow = MainWindow(root, im_original)

    root.mainloop()
    #root.destroy()

if __name__ == "__main__":
    main()
