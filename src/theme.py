import configparser


class Theme:

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
            rgb_list = rgb_list + [int(color[i:i+2], 16) for i in (0, 2, 4)]
        return rgb_list

    def format_palette(self, palette):
        if len(palette) < 256:
            return palette + [0, ] * (256-len(palette)) * 3
        return palette[:255]
