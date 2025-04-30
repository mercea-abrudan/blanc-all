import os
import platform
import shutil
import sys


def get_hosts_path():
    """Determines the correct hosts file path based on the OS."""
    if platform.system() == "Windows":
        return "C:\\Windows\\System32\\drivers\\etc\\hosts"
    else:
        print(f"Unsupported operating system: {platform.system()}")
        sys.exit(1)
    
def copy_file(source: str | os.PathLike, destination: str | os.PathLike):
    """
    Copies a file from the source path to the destination path.

    Args:
        source (str | os.PathLike): The file path of the source file.
        destination (str | os.PathLike): The file path of the destination.

    Returns:
        None
    """
    if os.path.isfile(destination):
        print(f"File already exists at {destination}. Copy operation skipped.")
    else:
        try:
            shutil.copy(source, destination)
            print(f"File copied successfully from:to\n{source}\n{os.path.abspath(destination)}")
        except FileNotFoundError:
            print(f"Error: The source file '{source}' was not found.")
        except PermissionError:
            print("Error: Permission denied. Please check your access rights.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
