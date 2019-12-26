from PIL import Image as Img, ImageFilter, ImageChops
import cv2
import numpy as np
import math


class Image:

    def __init__(self, file_path, palette, kernel_size, glitch):
        self.kernel_size = kernel_size
        self.kernel = (kernel_size, kernel_size)
        self.glitch = glitch
        self.palette(palette)
        self.open(file_path)
        self.apply()

    def palette(self, palette):
        self.pimage = Img.new('P', (1, 1), 0)
        self.pimage.putpalette(palette)

    def open(self, file_path):
        self.file = Img.open(file_path)
        self.file.convert('RGB')

    def apply(self):
        self.result = self.file.quantize(palette=self.pimage)
        self.result = self.result.convert('RGB')
        if self.glitch:
            width, height = self.result.size
            height_resize = height - self.glitch
            maxsize = (math.ceil((width/height) *
                                 height_resize), height_resize)

            width_shift = math.ceil((width - maxsize[0])/2)
            height_shift = math.ceil((height - maxsize[1])/2)
            left_border = width_shift
            top_border = height_shift
            right_border = maxsize[0] + left_border
            bottom_border = maxsize[1] + top_border

            crop_box = (left_border, top_border, right_border, bottom_border)

            r, g, b = self.result.split()

            g.thumbnail(maxsize)
            r = r.crop(crop_box)
            b = b.crop(crop_box)

            self.result = Img.merge('RGB', (r, g, b))
        if self.kernel_size > 0:
            np_image = np.asarray(self.result).astype(np.uint8)
            np_image = cv2.GaussianBlur(np_image, self.kernel, 0)
            self.result = Img.fromarray(np_image)

    def show(self):
        self.result.show()

    def save(self, file_path):
        self.result.save(file_path)
