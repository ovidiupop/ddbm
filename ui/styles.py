# styles.py
from tkinter import ttk


def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Sau 'alt', 'default', 'classic' în funcție de preferințe

    # Definirea stilurilor de bază
    base_style = {
        'font': ('Helvetica', 10),
        'padding': 5
    }

    # Aplicarea stilurilor de bază pentru widget-uri comune
    for widget in ['TLabel', 'TButton', 'TCheckbutton', 'TEntry']:
        style.configure(widget, **base_style)

    # Configurări specifice
    style.configure('TFrame', padding=10)
    style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))

    # Stiluri pentru butoane
    button_styles = {
        'Primary.TButton': ('#4CAF50', '#45a049'),  # (normal, active)
        'Secondary.TButton': ('#f44336', '#da190b')
    }

    for btn_style, (normal_bg, active_bg) in button_styles.items():
        style.configure(btn_style, background=normal_bg, foreground='white')
        style.map(btn_style,
                  background=[('active', active_bg)],
                  foreground=[('active', 'white')])

    # Stil pentru butoanele din bara de instrumente
    style.configure('Toolbar.TButton', padding=5)
