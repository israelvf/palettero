from theme import Theme
from image import Image
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
    palette = Theme(theme).palette

    if os.path.isdir(args.input):
        directory = os.fsencode(args.input)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
                file_path = os.path.join(args.input, filename)
                output = args.output if args.output else os.path.join(
                    args.input, filename.split(".")[0] + "_edt." + filename.split(".")[1])
                if os.path.isdir(output):
                    output = os.path.join(output, filename)
                Image(file_path, palette, args.smooth,
                      args.glitch).save(output)
            else:
                continue
    elif os.path.isfile(args.input):
        if args.input.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            output = args.output if args.output else args.input.split(
                ".")[0] + "_edt." + args.input.split(".")[1]
            if os.path.isdir(output):
                file_dir, filename = os.path.split(args.input)
                output = os.path.join(output, filename)
            Image(args.input, palette, args.smooth, args.glitch).save(output)
    else:
        parser.error("input must be a valid file or a directory")
