from PIL import Image, ImageFilter, ImageChops
import cv2
import numpy as np
import math


class ImageHandler:

    def __init__(self, file_path, palette, smooth, glitch):
        self.smooth = smooth
        self.glitch = glitch
        self.palette(palette)
        self.open(file_path)
        self.apply()

    def palette(self, palette):
        self.pimage = Image.new('P', (1, 1), 0)
        self.pimage.putpalette(palette)

    def open(self, file_path):
        self.file = Image.open(file_path)
        self.file.convert('RGB')
        if self.file.mode == 'RGBA':
            background = Image.new("RGB", self.file.size, (255, 255, 255))
            background.paste(self.file, mask=self.file.split()[3])
            self.file = background

    def apply(self):
        self.result = self.file.quantize(palette=self.pimage)
        self.result = self.result.convert('RGB')
        if self.glitch:
            width, height = self.result.size
            height_resize = height - self.glitch
            maxsize = (math.ceil((width/height) *
                                 height_resize), height_resize)

            left_border = math.ceil((width - maxsize[0])/2)
            top_border = math.ceil((height - maxsize[1])/2)
            right_border = maxsize[0] + left_border
            bottom_border = maxsize[1] + top_border

            crop_box = (left_border, top_border, right_border, bottom_border)

            r, g, b = self.result.split()

            g.thumbnail(maxsize)
            r = r.crop(crop_box)
            b = b.crop(crop_box)

            self.result = Image.merge('RGB', (r, g, b))
            self.result = self.result.resize((width, height))
        if self.smooth:
            np_image = np.asarray(self.result).astype(np.uint8)
            np_image = cv2.bilateralFilter(np_image, 3, 300, 20)
            self.result = Image.fromarray(np_image)

    def show(self):
        self.result.show()

    def save(self, file_path):
        self.result.save(file_path)
