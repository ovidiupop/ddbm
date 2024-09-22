# main.py
import tkinter as tk

from config_manager import ensure_config_exists
from main_window import MainWindow
from styles import apply_styles


def main():
    # Asigură-te că toate fișierele de configurare necesare există
    ensure_config_exists()

    # Inițializează fereastra principală Tkinter
    root = tk.Tk()

    # Aplică stilurile definite
    apply_styles()

    # Creează și afișează fereastra principală a aplicației
    MainWindow(root)

    # Începe bucla principală a aplicației
    root.mainloop()

if __name__ == "__main__":
    main()
