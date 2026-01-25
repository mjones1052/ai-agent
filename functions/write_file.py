import os
from os import path
import types
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if path.isdir(file_path) == True:
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')
        directory, filename = os.path.split(target_file)
        os.makedirs(directory, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return str(e)
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)