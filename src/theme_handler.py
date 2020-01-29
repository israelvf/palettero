import configparser
from math import sqrt


class ThemeHandler:

    def __init__(self, file):
        hex_palette = self.load_palette(file)
        rgb_palette = self.hex_to_rgb(hex_palette)
        self.palette = self.format_palette(rgb_palette)

    def load_palette(self, file):
        palette = []
        palette_file = configparser.ConfigParser()
        palette_file.read(file)
        for color in palette_file['colors']:
            palette.append(palette_file['colors'][color].lstrip('#'))
        return palette

    def hex_to_rgb(self, palette):
        rgb_list = []
        for color in palette:
            rgb_list += [int(color[i:i+2], 16) for i in (0, 2, 4)]
        return rgb_list

    def find_darkest_color(self, palette):
        rgb_colors = []
        rgb_color = []
        module = []
        for channel in palette:
            rgb_color += [channel]
            if len(rgb_color) == 3:
                rgb_colors += [rgb_color]
                rgb_color = []
        if rgb_color:
            rgb_colors += [rgb_color]
        for color in rgb_colors:
            module += [sqrt(color[0]**2 + color[1]**2 + color[2]**2)]
        darkest_index = module.index(min(module))
        return rgb_colors[darkest_index]

    def format_palette(self, palette):
        if len(palette) < 256:
            darkest_color = self.find_darkest_color(palette)
            return palette + darkest_color * (256-len(palette))
        return palette[:255]
