import os
from os import path
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if path.isfile(target_file) == False:
            raise ValueError(f'Error: File not found or is not a regular file: "{file_path}"')
        # After reading the first MAX_CHARS...
        f = open(target_file)
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        content = str(e)
    return content