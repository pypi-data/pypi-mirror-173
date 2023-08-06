"""Screenshot Taker"""
import sys
import os
import time
import random
from random import choice
from string import digits

import tkinter
from tkinter import ttk

from PIL import Image, ImageTk, ImageGrab
from PIL.PngImagePlugin import PngImageFile, PngInfo

from .engine_util import locate_all
from .engine_util import LARGE_FONT, NORM_FONT, SMALL_FONT, REGION_PICK_VIEW, OFFSET_PICK_VIEW, SIMILARITY_PICK_VIEW, NAME_PICK_VIEW

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
REL_PATH = "my_screenshot.png"
abs_file_path = os.path.join(script_dir, REL_PATH)
SCREENSHOT = abs_file_path


class ScreenShotTaker():
    """
    Class to manage screenshot selecting process,
    draws the screenshot on a canvas where a region is selected along with
    an offset and matching confidence.
    """

    def __init__(self, master, save_location, needle='', haystack=SCREENSHOT, editing=False,
                 temp_screenshot_path='my_screenshot.png'):
        """
        Initialize values and prepare the region pick view
        """
        self.w4 = None
        self.w2 = None
        self.w3 = None
        self.button_check = None
        self.save_location = save_location
        self.needle = needle
        self.haystack = haystack
        self.editing = editing
        self.screenshot_id = ''.join(choice(digits) for i in range(12))
        self.save_path = ''.join([save_location, "/img/aai_", self.screenshot_id, ".png"])
        self.file_name = ''.join(['aai_', self.screenshot_id])
        self.master = master
        self.master.title("AAI Image Extractor")

        if self.editing:
            self.init_canvas_screenshot(self.needle)
        else:
            self.init_canvas_screenshot(self.haystack)

        self.button = ttk.Button(master, text="Confirm region", command=self.view_offset_picker, style='Accent.TButton')
        self.button.pack(side=tkinter.BOTTOM, pady=20)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.x = self.y = 0

        if self.editing:
            self.view_offset_picker()
        else:
            self.lower_confidence = 0.5
            self.upper_confidence = 1
            self.confidence_step_size = 0.05
            self.view = REGION_PICK_VIEW

            self.offset_x = 0
            self.offset_y = 0

            self.canvas.bind("<ButtonPress-1>", self.on_button_press_rectangle)
            self.canvas.bind("<B1-Motion>", self.on_move_press)

    def view_offset_picker(self):
        """
        View to choose the offset to be used,
        saved as offset to center of the selected region
        """
        self.view = OFFSET_PICK_VIEW
        self.canvas.delete(self.screenshot)
        self.button.configure(text="Confirm offset!", command=lambda: self.view_confidence_picker())
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press_offset)

        # cropping screenshot to selected region
        if not self.editing:
            ratio = self.original_im.size[0] / self.img.size[0]
            self.ratio = ratio
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            left = x1 * ratio
            top = y1 * ratio
            right = x2 * ratio
            bottom = y2 * ratio
            self.cropped = self.original_im.crop((left, top, right, bottom))
            self.cropped.save('my_cropped.png', 'PNG')
            self.tk_cropped = ImageTk.PhotoImage(self.cropped, master=self.master)
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.w = w
            self.h = h

            w = w / 4
            h = h / 4
            self.selected_region = self.canvas.create_image(w, h, image=self.tk_cropped)

            # drawing default cross at center
            self.cross_h = self.canvas.create_line(w - 10, h, w + 10, h, fill='red')
            self.cross_v = self.canvas.create_line(w, h - 10, w, h + 10, fill='red')

            # center of img
            self.offset_x = self.w / 4  # was / 2
            self.offset_y = self.h / 4  # was / 2 (should a bug occur)

            self.canvas.delete(self.rect)

        else:
            self.cropped = self.original_im
            self.cropped.save('my_cropped.png', 'PNG')
            self.tk_cropped = ImageTk.PhotoImage(self.img, master=self.master)
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.w = w
            self.h = h
            w = w / 4
            h = h / 4
            self.selected_region = self.canvas.create_image(w, h, image=self.tk_cropped)

            # drawing default cross at center
            target_image = PngImageFile(self.needle)
            print(target_image.text)
            self.offset_x = w + float(target_image.text["offset_x"])
            self.offset_y = h + float(target_image.text["offset_y"])
            self.cross_h = self.canvas.create_line(w - 10, h, w + 10, h, fill='red')
            self.cross_v = self.canvas.create_line(w, h - 10, w, h + 10, fill='red')

            self.canvas.coords(self.cross_h, self.offset_x - 10, self.offset_y, self.offset_x + 10, self.offset_y)
            self.canvas.coords(self.cross_v, self.offset_x, self.offset_y - 10, self.offset_x, self.offset_y + 10)

            self.canvas.delete(self.rect)

    def view_confidence_picker(self):
        """
        View showing the confidence picker
        """
        self.view = SIMILARITY_PICK_VIEW
        self.canvas.delete('all')
        for widget in self.master.winfo_children():
            widget.destroy()

        self.lower_confidence = 0.5
        self.upper_confidence = 1
        self.confidence_step_size = 0.05

        self.button = ttk.Button(self.master, text="Confirm confidence", command=self.view_name_picker,
                                 style='Accent.TButton')
        self.button_check = ttk.Button(self.master, text="Check", command=self.reset_confidence)
        # self.w2 = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL, command = lambda val: (self.set_confidence(val)), length=200)

        self.w2 = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_lower_confidence(val)), length=200)
        self.w3 = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_upper_confidence(val)), length=200)
        self.w4 = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_confidence_step_size(val)), length=200)

        if not self.editing:
            self.w2.set(50)
            self.w3.set(100)
            self.w4.set(5)
        else:
            target_image = PngImageFile(self.needle)
            self.w2.set(int(float(target_image.text["lower_confidence"]) * 100))
            self.w3.set(int(float(target_image.text["upper_confidence"]) * 100))

        self.button.pack(side=tkinter.BOTTOM, padx=20, pady=20)
        self.button_check.pack(side=tkinter.BOTTOM, padx=20, pady=20)
        self.w4.pack(side=tkinter.BOTTOM)
        ttk.Label(self.master, text='Confidence step size', font=('sans-serif', 10)).pack(side=tkinter.BOTTOM)
        self.w3.pack(side=tkinter.BOTTOM)
        ttk.Label(self.master, text='Upper confidence', font=('sans-serif', 10)).pack(side=tkinter.BOTTOM)
        self.w2.pack(side=tkinter.BOTTOM)
        ttk.Label(self.master, text='Lower confidence', font=('sans-serif', 10)).pack(side=tkinter.BOTTOM)
        self.init_canvas_screenshot(self.haystack)

    def view_name_picker(self):
        """
        View showing the name picker
        """
        self.view = NAME_PICK_VIEW
        self.canvas.delete('all')
        for widget in self.master.winfo_children():
            widget.destroy()
        self.button = ttk.Button(self.master, text="Confirm name", command=self.confirm_name, style='Accent.TButton')
        self.text_box = ttk.Entry(self.master)
        self.text_box.insert(tkinter.END, self.file_name)
        self.button.pack(side=tkinter.BOTTOM, padx=20, pady=20)
        self.text_box.pack(side=tkinter.BOTTOM, pady=(20, 0))
        self.init_canvas_cropped()

    def init_canvas_screenshot(self, haystack):
        """
        Initialize the canvas to take remaining space on screen, filled with screenshot
        """
        w, h = self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2
        self.master.focus_set()
        self.master.bind("<Return>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas = tkinter.Canvas(self.master, width=w, height=h, cursor="cross")
        self.canvas.pack()
        self.canvas.configure(background='black')
        print("Haystack: ", haystack)
        self.original_im = Image.open(haystack)
        self.img = Image.open(haystack)
        img_width, img_height = self.img.size
        img_width = img_width
        img_height = img_height
        if img_width > w or img_height > h:
            ratio = min(w/img_width, h/img_height)
            img_width = int(img_width*ratio)
            img_height = int(img_height*ratio)
            self.img = self.img.resize((img_width,img_height), Image.ANTIALIAS)

        self.wazil,self.lard=self.img.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.img, master=self.master)
        print("Screenshot HAYSTACK", haystack)
        self.screenshot = self.canvas.create_image(w/2, h/2, image=self.tk_im)


    def init_canvas_cropped(self):
        """
        Initialize the canvas to take remaining space on screen, filled with screenshot
        """
        w, h = self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2
        self.master.focus_set()
        self.master.bind("<Return>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas = tkinter.Canvas(self.master, width=w, height=h, cursor="cross")
        self.canvas.pack()
        self.canvas.configure(background='black')
        self.original_im = Image.open("my_cropped.png")
        self.img = Image.open("my_cropped.png")
        img_width, img_height = self.img.size
        if img_width > w or img_height > h:
            ratio = min(w/img_width, h/img_height)
            img_width = int(img_width*ratio)
            img_height = int(img_height*ratio)
            self.img = self.img.resize((img_width,img_height), Image.ANTIALIAS)

        self.wazil,self.lard=self.img.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.img, master=self.master)
        self.screenshot = self.canvas.create_image(w/2,h/2,image=self.tk_im)

    def confirm_name(self):
        """
        Confirm the name and save the selected region to a png
        with the chosen confidence and offsets to the center as metadata

        This metadata can be retrieved through the text field of
        PngImageFile("my_image_meta.png")
        """
        metadata = PngInfo()
        metadata.add_text("offset_x", str(self.offset_x - self.w / 4))
        metadata.add_text("offset_y", str(self.offset_y - self.h / 4))
        metadata.add_text("lower_confidence", str(self.lower_confidence))
        metadata.add_text("upper_confidence", str(self.upper_confidence))
        metadata.add_text("confidence_step_size", str(self.confidence_step_size))

        self.save_path = ''.join([self.save_location, '/', self.text_box.get().strip(), ".png"])

        print("Save path: ")
        print(self.save_path)

        self.cropped.save(self.save_path, pnginfo=metadata)
        target_image = PngImageFile(self.save_path)
        print(target_image.text)
        self.master.destroy()

    def set_upper_confidence(self, val):
        """setter"""
        self.upper_confidence = float(val) / 100.0

    def set_lower_confidence(self, val):
        """setter"""
        self.lower_confidence = float(val) / 100.0

    def set_confidence_step_size(self, val):
        """setter"""
        self.confidence_step_size = float(val) / 100.0

    def reset_confidence(self):
        """
        Recalculates matching regions
        """
        # self.confidence = float(self.confidence) / 100.0
        try:
            for match in self.matches:
                self.canvas.delete(match)
        except AttributeError:
            pass

        self.calculate_all_matches()
        print(self.lower_confidence)

    def calculate_all_matches(self):
        """
        Calculates all the matching regions in the taken screenshot, displays these
        regions with red rectangles
        """

        confidence_float = float(self.lower_confidence)
        imloc = locate_all('my_cropped.png', self.haystack, confidence=confidence_float)
        self.matches = []
        self.ratio = self.original_im.size[0] / self.img.size[0]
        for coords in imloc:
            left, top, width, height = coords
            left = left / self.ratio
            top = top / self.ratio
            width = width / self.ratio
            height = height / self.ratio
            match = self.canvas.create_rectangle(left, top, left + width, top + height, fill="", outline="red")
            self.matches.append(match)

    def on_button_press_rectangle(self, event):
        """ Starts a new rectangle """
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="", outline="red")

    def on_button_press_offset(self, event):
        """ Draws a cross at the clicked coordinates and saves the offsets """
        self.offset_x = event.x
        self.offset_y = event.y
        self.canvas.coords(self.cross_h, self.offset_x - 10, self.offset_y, self.offset_x + 10, self.offset_y)
        self.canvas.coords(self.cross_v, self.offset_x, self.offset_y - 10, self.offset_x, self.offset_y + 10)

    def on_move_press(self, event):
        """ Updates the rectangle to match the current selected region """
        cur_x, cur_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
