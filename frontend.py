# http://effbot.org/tkinterbook/tkinter-hello-again.htm

import sys
import random
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master, im):
        frame = tk.Frame(master)
        frame.grid()

        # picture
        self.images = [im]
        self.img_index = 0
        self.photo = ImageTk.PhotoImage(self.images[self.img_index])
        self.imglabel = tk.Label(frame, image=self.photo)

        # do interesting shit button
        self.drawbutton = tk.Button(
            frame,
            text="do stuff",
            command=self.draw
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
            command=self.increment_ind
        )

        self.indexlabel = tk.Label(
            frame,
            text=str(self.img_index)
        )

        # pack everything into a nice grid layout
        self.imglabel.grid(column=0, row=0, columnspan=3, rowspan=2)

        self.undobutton.grid(column=0, row=2)
        self.indexlabel.grid(column=1, row=2)
        self.redobutton.grid(column=2, row=2)

        self.drawbutton.grid(column=3, row=0)

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

        # insert logic about what to draw
        self.sort_pairs_vert(im)

        self.drawbutton.config(state=tk.NORMAL)

    def redraw(self):
        self.photo = ImageTk.PhotoImage(self.images[self.img_index])
        self.imglabel.config(image=self.photo)
        self.imglabel.update_idletasks()

    def sort_pairs_vert(self, im, rounds=30):
        for i in range(rounds):
            for _ in range(im.size[0]*im.size[1]//40):
                x = random.randrange(0, im.size[0]-2)
                y = random.randrange(0, im.size[1]-2)

                if weight(*im.getpixel((x, y))) < \
                   weight(*im.getpixel((x, y+1))):
                    tmp = im.getpixel((x, y))
                    im.putpixel((x, y), im.getpixel((x, y+1)))
                    im.putpixel((x, y+1), tmp)
            self.redraw()

def weight(r,g,b):
    return r**2 + g**2 + b**2

def main():
    root = tk.Tk()
    im_original = Image.open(sys.argv[1]).convert("RGB")
    mainWindow = MainWindow(root, im_original)

    root.mainloop()
    #root.destroy()

if __name__ == "__main__":
    main()
