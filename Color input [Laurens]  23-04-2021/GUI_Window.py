import tkinter as tk
import tkinter.font as tkFont
import GUI_Buttons as GB
import sys
from PIL import Image, ImageTk

# rgb to hex conv.   -> '#%02x%02x%02x' % (0, 128, 64)

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1280x720')

        # setting title
        self.root.title("[Specto] Initial color setup V1.2")

        # setting window size
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="#f0f0f0")

        # Specto tkinter icon
        self.root.iconbitmap('specto_icon.ico')

        #Specto small image import
        specto_image = Image.open('small_specto.png')
        specto_image = ImageTk.PhotoImage(specto_image)
        self.specto_label = tk.Label(self.root, image=specto_image)
        self.specto_label.image = specto_image
        self.specto_label.place(x=15, y=-8, width=200, height=60)

        # Close window def
        self.root.bind('<Escape>', sys.exit)

        # Enter press to enter button
        self.root.bind('<Return>', GB.FilterCount.numberCheck)


        # picture background color
        self.layout_box = tk.Label(self.root)
        self.layout_box["bg"] = "#e0e0e0"
        self.layout_box.place(x=25, y=45, width=800, height=645)

        # Insert buttons
        self.filter_generator = GB.FilterCount(self.root)
        self.import_button = GB.ImageImport(self.root)
        self.next_button = GB.output(self.root)

        # self.filter_generator.filter_list{'filter0'}.rgbs

        # start loop
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
