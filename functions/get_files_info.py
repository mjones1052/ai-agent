from os import path
import os


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if path.isdir(target_dir) == False:
            raise ValueError(f'Error: "{directory}" is not a directory')
        file_info = str()
        for item in os.listdir(target_dir):
            item_path = path.join(target_dir, item)
            if path.isfile(item_path):
                size = path.getsize(item_path)
                file_info += f" - {item}: file_size={size} bytes, is_dir=False\n"
            elif path.isdir(item_path):
                size = path.getsize(item_path)
                file_info += f" - {item}: file_size={size} bytes, is_dir=True\n"
        return file_info
    except Exception as e:
        return str(e)