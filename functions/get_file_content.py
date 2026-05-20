import os
from config import MAX_CHARS


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
