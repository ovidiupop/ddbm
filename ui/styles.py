import tkinter as tk
from tkinter import ttk


def apply_styles():
    style = ttk.Style()

    # Stilul pentru butonul principal (Save)
    style.configure('Primary.TButton',
                    background='#007bff',
                    foreground='white',
                    padding=(10, 5))

    # Stilul pentru butonul de pericol (Cancel)
    style.configure('Danger.TButton',
                    background='#dc3545',
                    foreground='white',
                    padding=(10, 5))

    # Stilul pentru butonul secundar (dacă este necesar)
    style.configure('Secondary.TButton',
                    background='#6c757d',
                    foreground='white',
                    padding=(10, 5))

    # Adăugați aici alte stiluri pentru aplicație, dacă este necesar