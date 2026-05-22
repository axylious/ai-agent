import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Lists file contents in a specified directory relative to the working directory, providing content. Content will be truncated if over {MAX_CHARS} characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list file contents from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING, description="File endpoint"
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)

    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = (
        os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    )

    if not valid_target_path:
        print(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )
    else:
        if not os.path.isdir(target_path):
            try:
                with open(target_path, "r") as f:
                    contents = f.read(MAX_CHARS)
                    if f.read(1):
                        contents += f'[...File "{file_path}" truncated at {MAX_CHARS}'
                    return contents
            except FileNotFoundError:
                print(f"Error: File not found or is not a regular file: {file_path}")
        else:
            print(f"Error: File not found or is not a regular file: {file_path}")
