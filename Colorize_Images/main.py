import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use('Agg')

# For display issues (to handle environments without display support)
import sys
import os

if os.environ.get('DISPLAY','') == '':
    #print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

# Load numpy file and model
numpy_file = np.load('./pts_in_hull.npy')
Caffe_net = cv.dnn.readNetFromCaffe("./models/colorization_deploy_v2.prototxt", "./models/colorization_release_v2.caffemodel")
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.pos = []
        self.master.title("B&W Image Colorization")
        self.pack(fill=BOTH, expand=1)

        # Menu for the application
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Upload Image", command=self.uploadImage)
        file.add_command(label="Color Image", command=self.color)
        menu.add_cascade(label="File", menu=file)

        self.canvas = tk.Canvas(self, width=300, height=400, bg='white')

        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image = None
        self.image2 = None

    def uploadImage(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd())
        if not filename:
            return
        load = Image.open(filename)
        load = load.resize((480, 360), Image.Resampling.LANCZOS)

        if self.image is None:
            w, h = load.size
            width, height = root.winfo_width(), root.winfo_height()
            self.render = ImageTk.PhotoImage(load)
            self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)
        else:
            self.canvas.delete(self.image2)
            w, h = load.size
            width, height = root.winfo_screenmmwidth(), root.winfo_screenheight()
            self.render2 = ImageTk.PhotoImage(load)
            self.image2 = self.canvas.create_image((w / 2, h / 2), image=self.render2)

        frame = cv.imread(filename)

        # Adjust the model's layers
        Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [numpy_file.astype(np.float32)]
        Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

        # Image processing for colorization
        input_width = 224
        input_height = 224
        rgb_img = (frame[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
        lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
        l_channel = lab_img[:, :, 0]

        # Resize and adjust the L channel
        l_channel_resize = cv.resize(l_channel, (input_width, input_height))
        l_channel_resize -= 50

        # Forward pass through the model
        Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
        ab_channel = Caffe_net.forward()[0, :, :, :].transpose((1, 2, 0))

        # Resize output to original image size
        (original_height, original_width) = rgb_img.shape[:2]
        ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
        lab_output = np.concatenate((l_channel[:, :, np.newaxis], ab_channel_us), axis=2)
        bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)

        # Save the result
        cv.imwrite("./result.png", (bgr_output * 255).astype(np.uint8))
        print("Saved result.png successfully")

    def color(self):
        result_path = "./result.png"
        if os.path.exists(result_path):
            load = Image.open(result_path)
            load = load.resize((480, 360), Image.Resampling.LANCZOS)

            if self.image is None:
                w, h = load.size
                self.render = ImageTk.PhotoImage(load)
                self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)
                root.geometry("%dx%d" % (w, h))
            else:
                w, h = load.size
                width, height = root.winfo_screenmmwidth(), root.winfo_screenheight()
                self.render3 = ImageTk.PhotoImage(load)
                self.image3 = self.canvas.create_image((w / 2, h / 2), image=self.render3)
                self.canvas.move(self.image3, 500, 0)
        else:
            print("Error: result.png not found. Please check if the colorization process completed successfully.")

# Initialize the main Tkinter window
root = tk.Tk()
root.geometry("%dx%d" % (980, 600))
root.title("B&W Image Colorization GUI")

app = Window(root)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()
