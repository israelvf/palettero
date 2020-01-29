import os


class FileHandler:

    def __init__(self, input_path, output_path=None):
        self.input_path = input_path
        self.output_path = output_path
        self.SUPPORTED_EXTENSIONS = (
            ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")

    def get_files_from_folder(self):
        if not os.path.isdir(self.input_path):
            return
        path_list = []
        directory = os.fsencode(self.input_path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if not filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
                continue
            file_path = os.path.join(self.input_path, filename)
            output = self.output_path if self.output_path else os.path.join(
                self.input_path, filename.split(".")[0] + "_edt." + filename.split(".")[1])
            if os.path.isdir(output):
                output = os.path.join(output, filename)
            path_list.append((file_path, output))
        return path_list

    def get_files_from_file(self):
        if not os.path.isfile(self.input_path):
            return
        file_dir, filename = os.path.split(self.input_path)
        if self.input_path.lower().endswith(self.SUPPORTED_EXTENSIONS):
            output = self.output_path if self.output_path else self.input_path.split(
                ".")[0] + "_edt." + self.input_path.split(".")[1]
            if output == file_dir:
                output = self.input_path.split(
                    ".")[0] + "_edt." + self.input_path.split(".")[1]
            if os.path.isdir(output):
                output = os.path.join(output, filename)
            return [(self.input_path, output)]
