import os
from os import path
import subprocess
import types
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_file]) == absolute_path
        absolute_file_path = os.path.abspath(target_file)
        if not valid_target_dir:
            raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if path.isfile(absolute_file_path) != True:
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')
        if file_path.endswith('.py') == False:
            raise ValueError(f'Error: "{file_path}" is not a Python file')
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, check=True, text=True, capture_output=True, cwd=absolute_path, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f"Process exited with code {result.returncode}")
        elif result.stderr or result.stdout is None:
            raise RuntimeError("No output produced")
        else:
            return {"STDOUT:": result.stdout, "STDERR:": result.stderr}
    except Exception as e:
        return {f"Error: executing Python file: {e}"}

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)