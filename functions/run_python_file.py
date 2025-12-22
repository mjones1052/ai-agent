import os
from os import path

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if path.isfile(file_path) == True:
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')
        if file_path.endswith('.py') == False:
            raise ValueError(f'Error: "{file_path}" is not a Python file')
        command = ["python", absolute_path]