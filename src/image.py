from PIL import Image as Img, ImageFilter
import cv2
import numpy as np


class Image:

    def __init__(self, file_path, palette, kernel_size):
        self.kernel_size = kernel_size
        self.kernel = (kernel_size, kernel_size)
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
        if self.kernel_size > 0:
            np_image = np.asarray(self.result).astype(np.uint8)
            np_image = cv2.GaussianBlur(np_image, self.kernel, 0)
            self.result = Img.fromarray(np_image)

    def show(self):
        self.result.show()

    def save(self, file_path):
        self.result.save(file_path)
