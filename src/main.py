from theme_handler import ThemeHandler
from image_handler import ImageHandler
from file_handler import FileHandler
import argparse
import os

parser = argparse.ArgumentParser()

required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

required.add_argument(
    "-i", "--input", type=str, help="input image path or directory to apply theme", required=True)
required.add_argument("-t", "--theme", type=str,
                      help="theme to apply in image", required=True)

optional.add_argument(
    "-s", "--smooth", help="smooth output image", action="store_true")
optional.add_argument(
    "-o", "--output", type=str, help="output image path or directory to save images")
optional.add_argument(
    "-g", "--glitch", type=int, help="add color glitch to image")

if __name__ == "__main__":
    args = parser.parse_args()

    main_dir, main_file = os.path.split(__file__)
    theme = os.path.join(main_dir, "themes", args.theme)
    if not os.path.isfile(theme):
        parser.error("theme must be a file in themes directory")
    palette = ThemeHandler(theme).palette
    file = FileHandler(args.input, args.output)
    path_list = []
    if os.path.isdir(args.input):
        path_list = file.get_files_from_folder()
    elif os.path.isfile(args.input):
        path_list = file.get_files_from_file()
    else:
        parser.error("input must be a valid file or a directory")

    for input_path, output_path in path_list:
        ImageHandler(input_path, palette, args.smooth,
                     args.glitch).save(output_path)
