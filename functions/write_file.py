import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)

    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    target_dir = os.path.dirname(target_path)
    valid_target_path = (
        os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    )

    if not valid_target_path:
        print(
            f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        )
    else:
        if not os.path.isdir(target_path):
            try:
                os.makedirs(target_dir, exist_ok=True)
                with open(target_path, "w") as f:
                    f.write(content)

                print(
                    f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                )
            except FileExistsError as err:
                print(f'Error: Directory "{target_path}" could not be created: {err}')
            except FileNotFoundError:
                print(f"Error: File not found or is not a regular file: {file_path}")
        else:
            print(f'Error: Cannot write to "{file_path}" as it is a directory')
