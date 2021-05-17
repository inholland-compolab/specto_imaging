import tkinter as tk
import tkinter.font as tkFont
import sys
from PIL import Image, ImageTk

import GUI_Buttons as GB


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1280x720')

        # setting title
        self.root.title("[Specto] Initial color setup V1.3 [ESC to close]")

        # Root title text inside window
        self.title_label = tk.Label(self.root)
        self.title_label["font"] = tkFont.Font(family='Arial', size=14)
        self.title_label["text"] = "Initial color setup"
        self.title_label.place(x=250, y=15)

        # setting window size
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="#f0f0f0")

        # Specto tkinter icon
        self.root.iconbitmap('specto_icon.ico')

        # Specto small image import
        specto_image = Image.open('small_specto.png')
        specto_image = ImageTk.PhotoImage(specto_image)
        self.specto_label = tk.Label(self.root, image=specto_image)
        self.specto_label.image = specto_image
        self.specto_label.place(x=15, y=-8, width=200, height=60)

        # Close root window def
        self.root.bind('<Escape>', sys.exit)

        # picture background color
        self.layout_box = tk.Label(self.root)
        self.layout_box["bg"] = "#e0e0e0"
        self.layout_box.place(x=25, y=45, width=800, height=645)

        # Insert buttons using GUI_Buttons code
        self.objects = {}
        self.objects["FilterCount"] = GB.FilterCount(self.root, self.objects)
        self.objects["ImageImport"] = GB.ImageImport(self.root, self.objects)
        self.objects["output"] = GB.output(self.root, self.objects)
        

        #self.filter_generator.filter_list{'filter0'}.rgbs

        # start loop
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
