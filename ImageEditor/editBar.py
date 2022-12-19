from tkinter import Frame, Button, LEFT
from tkinter import filedialog
from ImageEditor.forDelete.filterFrame import FilterFrame
from ImageEditor.forDelete.adjustFrame import AdjustFrame
import cv2


class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_button = Button(self, text="New",height = 4,width = 8,background="white")
        self.save_button = Button(self, text="Save",height = 4,width = 8,background="white")
        self.save_as_button = Button(self, text="Save As",height = 4,width = 8,background="white")
        self.draw_button = Button(self, text="Draw",height = 4,width = 8,background="white")
        self.clear_button = Button(self, text="Clear",height = 4,width = 8,background="white")

        self.black_Button = Button(self,height = 4,width = 8,background="black")
        self.red_Button = Button(self,height = 4,width = 8,background="red")
        self.blue_Button = Button(self,height = 4,width = 8,background="blue")
        self.green_Button = Button(self,height = 4,width = 8,background="green")

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.black_Button.bind("<ButtonRelease>", self.black_Button_released)
        self.red_Button.bind("<ButtonRelease>", self.red_Button_released)
        self.blue_Button.bind("<ButtonRelease>", self.blue_Button_released)
        self.green_Button.bind("<ButtonRelease>", self.green_Button_released)

        self.new_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.draw_button.pack(side=LEFT)
        self.clear_button.pack(side=LEFT)

        self.black_Button.pack(side=LEFT)
        self.red_Button.pack(side=LEFT)
        self.blue_Button.pack(side=LEFT)
        self.green_Button.pack(side=LEFT)




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



    def black_Button_released(self, event):
        self.master.drawColor = "black"
    def red_Button_released(self, event):
        self.master.drawColor = "red"
    def blue_Button_released(self, event):
        self.master.drawColor = "blue"
    def green_Button_released(self, event):
        self.master.drawColor = "green"