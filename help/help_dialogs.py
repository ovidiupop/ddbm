import os
import tkinter as tk
from tkinter import ttk, scrolledtext

def create_toplevel(parent, title, geometry=None):
    top = tk.Toplevel(parent)
    top.title(title)
    if geometry:
        top.geometry(geometry)
    top.transient(parent)
    top.grab_set()
    return top


def show_about(parent):
    about_window = create_toplevel(parent, "About Database Backup Manager", "300x200")
    about_window.resizable(False, False)

    about_frame = ttk.Frame(about_window, padding="20")
    about_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(about_frame, text="Database Backup Manager", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
    ttk.Label(about_frame, text="Version 1.0").pack()
    ttk.Label(about_frame, text="© 2024 Ovidiu Pop").pack()

    ttk.Button(about_frame, text="OK", command=about_window.destroy).pack(pady=(20, 0))


def show_info(parent):
    info_window = create_toplevel(parent, "Info", "600x400")
    info_window.minsize(400, 300)

    text_widget = scrolledtext.ScrolledText(info_window, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)

    # Path to the info.txt file in the help folder
    info_file_path = os.path.join('help', 'info.txt')

    try:
        with open(info_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            text_widget.insert(tk.END, content)
    except FileNotFoundError:
        text_widget.insert(tk.END, "The info.txt file was not found.")
    except Exception as e:
        text_widget.insert(tk.END, f"An error occurred while reading the file: {str(e)}")

    text_widget.config(state=tk.DISABLED)  # Make the text read-only

    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=10)

    return info_window
