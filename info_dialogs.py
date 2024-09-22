import tkinter as tk
from tkinter import ttk
from window_utils import create_toplevel

def show_about(parent):
    about_window = create_toplevel(parent, "About Database Backup Manager", "300x200")
    about_window.resizable(False, False)

    about_frame = ttk.Frame(about_window, padding="20")
    about_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(about_frame, text="Database Backup Manager", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
    ttk.Label(about_frame, text="Version 1.0").pack()
    ttk.Label(about_frame, text="© 2024 Ovidiu Pop").pack()

    ttk.Button(about_frame, text="OK", command=about_window.destroy).pack(pady=(20, 0))