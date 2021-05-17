import glob
import os
import os.path
import sys
import tkinter as tk
import tkinter.font as tkFont
from ctypes import windll
from tkinter import filedialog, StringVar, Entry, HORIZONTAL, VERTICAL
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

import GUI_Buttons as GB
import Filter_Calculations as FC


class Window:
    def __init__(self, objects):
        self.objects = objects
        self.root2 = tk.Toplevel()
        self.root2.geometry('1280x720')
        self.image = None
        self.image_frame = None
        self.image1 = None
        self.image1_frame = None



        # setting title
        self.root2.title("[Specto] Calculated export Image V1.0 [ESC to close]")

        # setting window size
        self.root2.resizable(width=False, height=False)
        self.root2.configure(bg="#f0f0f0")

        # Specto tkinter icon
        self.root2.iconbitmap('specto_icon.ico')

        # Specto small image import
        self.specto_image = Image.open('small_specto.png')
        self.specto_image = ImageTk.PhotoImage(self.specto_image)
        self.specto_label = tk.Label(self.root2, image=self.specto_image)
        self.specto_label.image = self.specto_image
        self.specto_label.place(x=15, y=-8, width=200, height=60)

        # Close root window def
        self.root2.bind('<Escape>', sys.exit)

        # picture background color
        self.layout_box = tk.Label(self.root2)
        self.layout_box["bg"] = "#e0e0e0"
        self.layout_box.place(x=25, y=45, width=1230, height=645)

        # Text inside window
        self.title_label = tk.Label(self.root2)
        self.title_label["font"] = tkFont.Font(family='Arial', size=14)
        self.title_label["text"] = "Calculated Go and NoGo Area's"
        self.title_label.place(x=250, y=15)

        self.origional_image_text = tk.Label(self.root2)
        self.origional_image_text["font"] = tkFont.Font(family='Arial', size=14)
        self.origional_image_text["text"] = "Input Image"
        self.origional_image_text.place(x=310, y=70)

        self.Export_image_text = tk.Label(self.root2)
        self.Export_image_text["font"] = tkFont.Font(family='Arial', size=14)
        self.Export_image_text["text"] = "Calculated output Image"
        self.Export_image_text.place(x=830, y=70)

        # button to selct import image
        self.path_button = tk.Button(self.root2)
        self.path_button["bg"] = "#E52E2B"
        self.path_button["font"] = tkFont.Font(family='Arial', size=10)
        self.path_button["fg"] = "#FFFFFF"
        self.path_button["relief"] = 'ridge'
        self.path_button["text"] = "Select Robot image location "
        self.path_button["command"] = self.browse_button
        self.path_button.place(x=265, y=660, width=180, height=25)

        #Button to Start calcualtion for export image
        self.perform_calculation_button = tk.Button(self.root2)
        self.perform_calculation_button["bg"] = "#E52E2B"
        self.perform_calculation_button["font"] = tkFont.Font(family='Arial', size=10)
        self.perform_calculation_button["fg"] = "#FFFFFF"
        self.perform_calculation_button["relief"] = 'ridge'
        self.perform_calculation_button["text"] = "Start performing calculation"
        self.perform_calculation_button["command"] = self.Output_Image_Import
        self.perform_calculation_button.place(x=850, y=660, width=180, height=25)

        self.calculation_busy = tk.Label(self.root2)

        self.root2.mainloop()





    def browse_button(self):
        global Auto_Image_Path
        self.Auto_Image_Path = askopenfilename()
        Auto_Image_Path = self.Auto_Image_Path
        self.Automatic_Image_Import()


    def Show_Calulating(self):
        self.calculation_busy["font"] = tkFont.Font(family='Arial', size=14)
        self.calculation_busy["text"] = "Calculating..."
        self.calculation_busy["bg"] = "#E0E0E0"
        self.calculation_busy.place(x=1020, y=660)
        self.root2.update()



    def Automatic_Image_Import(self):
        print("Before for loop with path: ", self.Auto_Image_Path)
        image_width = 500

        try:
            self.image = Image.open(self.Auto_Image_Path)

            if self.image_frame:
                self.image_frame.destroy()

            aspect_ratio = self.image.size[1] / self.image.size[0]
            self.image = self.image.resize((image_width, int(aspect_ratio * image_width)))

            if self.image.size[1] > 595:
                aspect_ratio = self.image.size[0] / self.image.size[1]
                self.image = self.image.resize((int(aspect_ratio * 595), 595))

            img = ImageTk.PhotoImage(self.image)
            self.image_frame = tk.Label(self.root2, image=img)
            self.image_frame.image = img
            self.image_frame.pack()
            self.image_frame.place(x=350 - self.image.size[0] // 2, y=367 - self.image.size[1] // 2, width=self.image.size[0], height=self.image.size[1])

        except:
            GB.popup('ERROR: Can not show import image')




    def Output_Image_Import(self):
        image1_width = 500

        try:
            Window.Show_Calulating(self)
            self.image1 = FC.colorCalculator(self.objects["FilterCount"].filter_list)

            if self.image1_frame:
                print("frame destroyed")
                self.image1_frame.destroy()

            aspect_ratio = self.image1.size[1] / self.image1.size[0]
            self.image1 = self.image1.resize((image1_width, int(aspect_ratio * image1_width)))

            if self.image1.size[1] > 595:
                print("image is > 595")
                aspect_ratio = self.image1.size[0] / self.image1.size[1]
                self.image1 = self.image1.resize((int(aspect_ratio * 595), 595))

            print("Image created ")
            img1 = ImageTk.PhotoImage(self.image1)
            self.image1_frame = tk.Label(self.root2, image=img1)
            self.image1_frame.image = img1
            self.image1_frame.pack()
            self.image1_frame.place(x=950 - self.image1.size[0] // 2, y=367 - self.image1.size[1] // 2, width=self.image1.size[0], height=self.image1.size[1])
            self.calculation_busy.destroy()


        except Exception as e:
            GB.popup('ERROR: Can not calculate export image. Check initial setup.')
            print(e)

if __name__ == "__main__":
    window = Window()
