from tkinter import Frame, Button, LEFT,Scale,Label,Entry
from tkinter import filedialog

import cv2
import tkinter as tk
from ImageEditor.Functionality import Functionality


class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.prevPos = 0

        self.new_button = Button(self, text="New",height = 4,width = 8,background="white")
        self.save_button = Button(self, text="Save",height = 4,width = 8,background="white")
        self.save_as_button = Button(self, text="Save As",height = 4,width = 8,background="white")
        self.draw_button = Button(self, text="Draw",height = 4,width = 8,background="white")
        self.clear_button = Button(self, text="Clear",height = 4,width = 8,background="white")

        self.black_Button = Button(self,height = 4,width = 8,background="black")
        self.red_Button = Button(self,height = 4,width = 8,background="red")
        self.blue_Button = Button(self,height = 4,width = 8,background="blue")
        self.green_Button = Button(self,height = 4,width = 8,background="green")

        self.position_Button = Button(self, text="Translate",height = 4,width=8, background="white")
        self.rotation_Button = Button(self, text="Rotate",height = 4,width=8, background="white")
        self.scale_up_Button = Button(self, text="Scale up",height = 2,width=8, background="white")
        self.scale_down_Button = Button(self, text="Scale down", height = 2,width=8, background="white")

        self.thickness_Slider = Scale(self,from_=1,to=10,orient=tk.HORIZONTAL,command=self.thickness_Slider_com)

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.black_Button.bind("<ButtonRelease>", self.black_Button_released)
        self.red_Button.bind("<ButtonRelease>", self.red_Button_released)
        self.blue_Button.bind("<ButtonRelease>", self.blue_Button_released)
        self.green_Button.bind("<ButtonRelease>", self.green_Button_released)

        self.position_Button.bind("<ButtonRelease>", self.Translate_Button_released)
        self.rotation_Button.bind("<ButtonRelease>", self.Rotate_Button_released)
        self.scale_up_Button.bind("<ButtonRelease>", self.Scale_Up_Button_released)
        self.scale_down_Button.bind("<ButtonRelease>", self.Scale_Down_Button_released)



        self.new_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.draw_button.pack(side=LEFT)
        self.clear_button.pack(side=LEFT)

        self.black_Button.pack(side=LEFT)
        self.red_Button.pack(side=LEFT)
        self.blue_Button.pack(side=LEFT)
        self.green_Button.pack(side=LEFT)
        self.position_Button.pack(side=tk.LEFT)
        self.rotation_Button.pack(side=tk.LEFT)
        self.scale_up_Button.pack(side=tk.TOP)
        self.scale_down_Button.pack(side=tk.TOP)

        self.thickness_Slider.pack()

    # Standard stuff
    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.image_viewer.deactivate_draw()


            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True
    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()

                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)
    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()

                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename
    def draw_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.configure(bg="white")
                else:
                    self.master.image_viewer.activate_draw()
                    self.draw_button.configure(bg="gray")
    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()

                self.master.processed_image = self.master.original_image.copy()
                self.master.image_viewer.show_image()

    # Color stuff
    def black_Button_released(self, event):
        self.master.drawColor = "black"
    def red_Button_released(self, event):
        self.master.drawColor = "red"
    def blue_Button_released(self, event):
        self.master.drawColor = "blue"
    def green_Button_released(self, event):
        self.master.drawColor = "green"

    # TransForm stuff
    def Translate_Button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.position_Button:
            if self.master.is_image_selected:
                self.master.processed_image = Functionality.Translate(self.master.processed_image,100,0)
                self.master.image_viewer.show_image()
    def Rotate_Button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotation_Button:
            if self.master.is_image_selected:
                self.master.processed_image = Functionality.Rotate(self.master.processed_image)
                self.master.image_viewer.show_image()
    def Scale_Up_Button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.scale_up_Button:
            if self.master.is_image_selected:
                self.master.processed_image = Functionality.Scale(self.master.processed_image, 1.2, 1.2)
                self.master.image_viewer.show_image()
    def Scale_Down_Button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.scale_down_Button:
            if self.master.is_image_selected:
                self.master.processed_image = Functionality.Scale(self.master.processed_image,0.8,0.8)
                self.master.image_viewer.show_image()
    def thickness_Slider_com(self,event):
        self.master.thickness = self.thickness_Slider.get()

