import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, StringVar, Entry, HORIZONTAL, VERTICAL
from ctypes import windll
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk
import sys

import GUI_Calculations as GC


# Setup buttons for amount of filters
class FilterCount:
    def __init__(self, root, objects):
        self.objects = objects
        self.root = root
        self.button = tk.Button(self.root)
        self.button["bg"] = "#E52E2B"
        self.button["font"] = tkFont.Font(family='Arial', size=10)
        self.button["fg"] = "#FFFFFF"
        self.button["relief"] = 'ridge'
        self.button["text"] = "Enter"
        self.button["command"] = self.numberCheck
        self.button.place(x=1100, y=10, width=150, height=20)

        self.label = tk.Label(self.root)
        self.label["font"] = tkFont.Font(family='Arial', size=10)
        self.label["text"] = "Amount of paint layers:"

        self.number = StringVar()
        self.label.place(x=900, y=5, width=140, height=30)
        self.txt_number = Entry(self.root, textvariable=self.number, width=5)
        self.txt_number.place(x=1050, y=10)

        self.layout_box = tk.Label(self.root)
        self.layout_box["bg"] = "#e0e0e0"
        self.layout_box.place(x=835, y=45, width=430, height=645)

        self.setMessage = lambda text: self.root.title('Color detection Software Specto V1.2:   %s' % text)

        # Enter press to enter button
        self.root.bind('<Return>', self.numberCheck)

        # Ctrl + f to print the created filters
        self.root.bind('<Control-f>', self.printFilters)

        button_dict = {}
        self.filter_list = {}

    # Shortcut for printing filters
    def printFilters(self, *args):
        print("Filter_list[] = {")
        for key, filter in self.filter_list.items():
            print("\t", key, filter.rgbs)
        print("}")

    # Check if input is valid number
    def numberCheck(self, *args):
        item = (self.number.get())
        if item.isdigit():
            if int(item) > 16:          # Max paint layers
                popup('ERROR: Maximum layers 16!')
                self.createButtons(16)
            elif int(item) == 0:        # paint layers cannot be 0
                popup('ERROR: Minimum layers 1!')
                self.createButtons(1)
            else:
                self.setMessage('INFO: Layer count updated!')   # valid numbers, create buttons
                self.createButtons(int(item))
        else:
            popup('ERROR: That input is not a valid number!')           # Check if non valid number is filled in

    def createButtons(self, filters):
        # acces rgbs values
        # for key in self.filter_list:
        # print(self.filter_list[filter0].rgbs)

        # update border hight
        self.layout_box.place(x=835, y=45, width=430, height= 33 + 36 * (filters + 1))
        temp_rgbs = 0

        if len(self.filter_list):
            temp_rgbs = self.filter_list[f'filter{len(self.filter_list) - 1}'].rgbs[:]
            self.filter_list[f'filter{len(self.filter_list) - 1}'].destroy()
            del self.filter_list[f'filter{len(self.filter_list) - 1}']

        for i in range(17):
            if i < filters and f'filter{i}' not in self.filter_list:
                self.filter_list[f'filter{i}'] = Filter(self.root, (855, 65 + 36 * i), i+1)

            if i == filters:
                if f'filter{i}' in self.filter_list:
                    self.filter_list[f'filter{i}'].destroy()
                    del self.filter_list[f'filter{i}']

                if temp_rgbs:
                    self.filter_list[f'filter{i}'] = Filter(self.root, (855, 65 + 36 * i), i+1, 'Composite', temp_rgbs)
                else:
                    self.filter_list[f'filter{i}'] = Filter(self.root, (855, 65 + 36 * i), i+1, 'Composite')

            if i > filters and f'filter{i}' in self.filter_list:
                self.filter_list[f'filter{i}'].destroy()
                del self.filter_list[f'filter{i}']


class Filter:
    # initial function for creating buttons
    def __init__(self, root, pos, index, name="", rgbs=(128, 128, 128, 20)):

        # variables
        self.rgbs = rgbs
        self.root = root

        # buttons
        self.button = tk.Button(root)
        self.button["bg"] = "#808080"
        self.button["font"] = tkFont.Font(family='Arial', size=10)
        self.button["fg"] = "#ffffff"
        self.button["relief"] = 'ridge'
        if not name == "": self.button["text"] = name
        else: self.button["text"] = "Paint layer %i" % index
        self.button["command"] = self.pressed
        self.button.place(x=pos[0], y=pos[1], width=150, height=25)

        # color indicators
        self.indicator = tk.Label(self.root)
        self.indicator["fg"] = "#333333"
        self.indicator["bg"] = ('#%02x%02x%02x' % self.rgbs[:3])
        self.indicator["borderwidth"] = 3
        self.indicator["relief"] = 'ridge'
        self.indicator.place(x=pos[0] + 170, y=pos[1], width=25, height=25)

        # color sliders for sensitivity
        self.slider = tk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL)
        self.slider.pack()
        self.slider.set(self.rgbs[3])
        self.slider["highlightbackground"] = "#e0e0e0"
        self.slider["bg"] = "#e0e0e0"
        self.slider["borderwidth"] = 0
        self.slider["command"] = self.sliderMoved
        self.slider.place(x=pos[0] + 215, y=pos[1] - 16, width=180)

    # Mouse buttons press
    def pressed(self):
        self.click_select = self.button["text"]
        self.root.bind('<Button-1>', self.colorPick)

    # update when slider moved
    def sliderMoved(self, var):
        self.rgbs = (self.rgbs[0], self.rgbs[1], self.rgbs[2], self.slider.get())

    # Screen color picker
    def colorPick(self, event):
        dc = windll.user32.GetDC(0)
        rgb = windll.gdi32.GetPixel(dc, event.x_root, event.y_root)
        r = rgb & 0xff
        g = (rgb >> 8) & 0xff
        b = (rgb >> 16)

        self.rgbs = (r, g, b, self.rgbs[3])
        self.indicator["bg"] = ('#%02x%02x%02x' % self.rgbs[:3])
        self.root.unbind('<Button-1>')

    # Reposition buttons
    def reposition(self, x, y):
        self.button.place(x=x, y=y, width=130, height=25)
        self.indicator.place(x=x+140, y=y, width=25, height=25)
        self.slider.place(x=x+180, y=y-18, width=150)

    # remove buttons
    def destroy(self):
        self.button.destroy()
        self.indicator.destroy()
        self.slider.destroy()
        del self

# import image
class ImageImport:
    def __init__(self, root, objects):
        self.objects = objects
        # variables
        self.root = root
        self.image = None
        self.image_frame = None
        self.height_limit = 550

        # Image import button
        self.button = tk.Button(root)
        self.button["bg"] = "#E52E2B"
        self.button["font"] = tkFont.Font(family='Arial', size=10)
        self.button["fg"] = "#FFFFFF"
        self.button["relief"] = 'ridge'
        self.button["text"] = "Open image for color picking"
        self.button["command"] = self.pressed
        self.button.place(x=625, y=10, width=200, height=25)
        self.setMessage = lambda text: self.root.title('[Specto] Initial color setup V1.3 [ESC to close]:   %s' % text)

    def pressed(self):
        image_path = tk.filedialog.askopenfilename()
        image_width = 750

        try:
            self.image = Image.open(image_path)

            if self.image_frame:
                self.image_frame.destroy()

            aspect_ratio = self.image.size[1] / self.image.size[0]
            self.image = self.image.resize((image_width, int(aspect_ratio * image_width)))

            if self.image.size[1] > 595:

                aspect_ratio = self.image.size[0] / self.image.size[1]
                self.image = self.image.resize((int(aspect_ratio * 595), 595))

            img = ImageTk.PhotoImage(self.image)
            self.image_frame = tk.Label(image=img)
            self.image_frame.image = img
            self.image_frame.pack()
            self.image_frame.place(x=425 - self.image.size[0] // 2, y=367 - self.image.size[1] // 2, width=self.image.size[0], height=self.image.size[1])

            self.setMessage('INFO: Image imported!')

        except:
            popup('ERROR: Importing file!')

    def reposition(self, x, y):
        self.button.place(x=x, y=y, width=130, height=25)

# popup notifiaction for errors
class popup:
    def __init__(self, text):
        self.root = tk.Tk()
        self.root.iconbitmap('specto_icon.ico')
        self.root.title("ERROR")

        height_popup = 80
        width_popup = 300
        self.root.geometry(f"{width_popup}x{height_popup}")
        self.label = tk.Label(self.root, text="{:^60}".format(text), wraplength = width_popup-20)
        self.label.place(x=17, y=8)

        self.button = tk.Button(self.root, text="Ok", command=self.root.destroy)
        self.button.place(x=0, y=55, width=width_popup, height=25)

        self.root.resizable(width=False, height=False)

        self.root.mainloop()

# export finish function
class output:
    def __init__(self, root, objects):
        self.objects = objects

        self.Auto_Image_Path = None
        self.calculation_window_button = tk.Button(root)
        self.calculation_window_button["bg"] = "#E52E2B"
        self.calculation_window_button["font"] = tkFont.Font(family='Arial', size=10)
        self.calculation_window_button["fg"] = "#FFFFFF"
        self.calculation_window_button["relief"] = 'ridge'
        self.calculation_window_button["text"] = "-> Open Calculation window"
        self.calculation_window_button["command"] = lambda: GC.Window(self.objects)
        self.calculation_window_button.place(x=1085, y=695, width=180, height=20)





