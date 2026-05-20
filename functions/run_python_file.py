import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)

    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = (
        os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    )

    if not valid_target_path:
        print(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
    else:
        if os.path.isfile(target_path):
            if file_path[-3:] == ".py":
                try:
                    command = ["python", target_path]
                    if args:
                        command.extend(args)
                    completed_process = subprocess.run(
                        command, capture_output=True, text=True, timeout=30
                    )
                    if completed_process.returncode != 0:
                        print(
                            f"Process exited with code {completed_process.returncode}"
                        )
                    if not completed_process.stdout and not completed_process.stderr:
                        print("No output produced")

                    if completed_process.stdout:
                        print(f"STDOUT: {completed_process.stdout}")
                    if completed_process.stderr:
                        print(f"STDERR: {completed_process.stderr}")
                except Exception as err:
                    print(f'Error: executing Python file: "{file_path}": {err}')
            else:
                print(f'"{file_path}" is not a Python file')
        else:
            print(f'Error: "{file_path}" does not exist or is not a regular file')
