import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tkinter as tk

from core.config_manager import ensure_config_exists
from main.main_window import MainWindow
from backup.backup_manager import execute_backup

def start_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

def main():
    ensure_config_exists()

    if len(sys.argv) > 1 and sys.argv[1] == "backup":
        # Rulează backup-ul fără GUI
        execute_backup()
    else:
        # Pornește interfața grafică normală
        start_gui()

if __name__ == "__main__":
    main()