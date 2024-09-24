import sys
import os
import tkinter as tk
from PIL import Image, ImageTk

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.config_manager import ensure_config_exists
from main.main_window import MainWindow
from backup.backup_manager import execute_backup


def start_gui():
    root = tk.Tk()
    root.title("DDBM")

    try:
        icon_path = "/usr/share/icons/hicolor/256x256/apps/ddbm.png"
        if os.path.exists(icon_path):
            icon = Image.open(icon_path)
            photo = ImageTk.PhotoImage(icon)
            root.wm_iconphoto(True, photo)
        else:
            print(f"Warning: Icon file not found at {icon_path}")
    except Exception as e:
        print(f"Error setting window icon: {e}")

    MainWindow(root)
    root.mainloop()


def main():
    ensure_config_exists()

    if len(sys.argv) > 1 and sys.argv[1] == "backup":
        # No GUI
        execute_backup()
    else:
        # GUI
        start_gui()


if __name__ == "__main__":
    main()
