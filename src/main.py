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
    "-s", "--smooth", type=int, help="smooth output image")
optional.add_argument(
    "-o", "--output", type=str, help="output image path or directory to save images")
optional.add_argument(
    "-g", "--glitch", type=int, help="add color glitch to image")

if __name__ == "__main__":
    kernel_size = 0
    args = parser.parse_args()

    main_dir, main_file = os.path.split(__file__)
    theme = os.path.join(main_dir, "themes", args.theme)
    if not os.path.isfile(theme):
        parser.error("theme must be a file in themes directory")
    palette = Theme(theme).palette

    if args.smooth:
        if args.smooth % 2 == 0:
            args.smooth += 1
        kernel_size = args.smooth

    if os.path.isdir(args.input):
        directory = os.fsencode(args.input)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".png"):
                file_path = os.path.join(args.input, filename)
                output = args.output if args.output else os.path.join(
                    args.input, filename[:-4] + "_edt" + filename[-4:])
                if os.path.isdir(output):
                    output = os.path.join(output, filename)
                Image(file_path, palette, kernel_size,
                      args.glitch).save(output)
            else:
                continue
    elif os.path.isfile(args.input):
        if args.input.lower().endswith(".jpg") or args.input.lower().endswith(".png"):
            output = args.output if args.output else args.input[:-
                                                                4] + "_edt" + args.input[-4:]
            if os.path.isdir(output):
                file_dir, filename = os.path.split(args.input)
                output = os.path.join(output, filename)
            Image(args.input, palette, kernel_size, args.glitch).save(output)
    else:
        parser.error("input must be a valid file or a directory")
