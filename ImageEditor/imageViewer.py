from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import cv2


class ImageViewer(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="gray", width=600, height=400)

        self.shown_image = None
        self.x = 0
        self.y = 0
        self.draw_ids = list()
        self.rectangle_id = 0
        self.ratio = 0

        self.canvas = Canvas(self, bg="gray", width=600, height=400)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_image(self, img=None):
        self.clear_canvas()

        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))

        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    def activate_draw(self):
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.master.is_draw_state = True

    def deactivate_draw(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.master.is_draw_state = False

    def start_draw(self, event):
        self.x = event.x
        self.y = event.y

    def draw(self, event):

        c = (0, 0, 0)
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=self.master.thickness,fill=self.master.drawColor, capstyle=ROUND, smooth=True))

        if self.master.drawColor == "black": c = (0,0,0)
        if self.master.drawColor == "red": c =   (0, 0, 255)
        if self.master.drawColor == "blue": c =  (255, 0, 0)
        if self.master.drawColor == "green": c = (0, 255, 0)

        cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),(int(event.x * self.ratio), int(event.y * self.ratio)),c, thickness=self.master.thickness,lineType=8)

        self.x = event.x
        self.y = event.y

    def clear_canvas(self):
        self.canvas.delete("all")
    def clear_draw(self):
        self.canvas.delete(self.draw_ids)
