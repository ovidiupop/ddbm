import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tkinter as tk

from core.config_manager import ensure_config_exists
from main.main_window import MainWindow
from ui.styles import apply_styles

def main():
    ensure_config_exists()
    root = tk.Tk()
    apply_styles()
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()