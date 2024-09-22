# file_utils.py
from tkinter import filedialog
import os

def browse_file(initial_path):
    """
    Open a file dialog to browse for a file.

    Args:
    initial_path (str): The initial path to start browsing from.

    Returns:
    str: The selected file path, or an empty string if no file was selected.
    """
    initial_dir = os.path.dirname(initial_path) if initial_path and os.path.exists(os.path.dirname(initial_path)) else os.path.expanduser("~")
    return filedialog.askopenfilename(initialdir=initial_dir)

def ensure_directory(path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
    path (str): The directory path to ensure.

    Returns:
    bool: True if the directory exists or was created successfully, False otherwise.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError:
        return False

def get_file_extension(filename):
    """
    Get the extension of a file.

    Args:
    filename (str): The name of the file.

    Returns:
    str: The file extension (without the dot), or an empty string if there's no extension.
    """
    return os.path.splitext(filename)[1][1:].lower()

def is_valid_file(filepath, allowed_extensions=None):
    """
    Check if a file exists and has an allowed extension.

    Args:
    filepath (str): The path to the file.
    allowed_extensions (list): A list of allowed file extensions (without the dot).

    Returns:
    bool: True if the file is valid, False otherwise.
    """
    if not os.path.isfile(filepath):
        return False
    if allowed_extensions is not None:
        return get_file_extension(filepath) in allowed_extensions
    return True
