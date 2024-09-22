import tkinter as tk
from tkinter import filedialog, messagebox

def create_toplevel(parent, title, geometry=None):
    top = tk.Toplevel(parent)
    top.title(title)
    if geometry:
        top.geometry(geometry)
    top.transient(parent)
    top.grab_set()
    return top


def adjust_window_size(window, main_frame=None, padding=20, max_size_ratio=0.8):
    window.update_idletasks()

    if main_frame:
        req_width = main_frame.winfo_reqwidth() + padding * 2
        req_height = main_frame.winfo_reqheight() + padding * 2
    else:
        req_width = window.winfo_reqwidth() + padding
        req_height = window.winfo_reqheight() + padding

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    max_width = int(screen_width * max_size_ratio)
    max_height = int(screen_height * max_size_ratio)

    new_width = min(req_width, max_width)
    new_height = min(req_height, max_height)

    window.geometry(f"{new_width}x{new_height}")

def show_info(parent, title, message):
    return messagebox.showinfo(title, message, parent=parent)

def show_error(parent, title, message):
    return messagebox.showerror(title, message, parent=parent)

def show_warning(parent, title, message):
    return messagebox.showwarning(title, message, parent=parent)

def ask_question(parent, title, message):
    return messagebox.askquestion(title, message, parent=parent)

def ask_ok_cancel(parent, title, message):
    return messagebox.askokcancel(title, message, parent=parent)

def ask_yes_no(parent, title, message):
    return messagebox.askyesno(title, message, parent=parent)

def ask_retry_cancel(parent, title, message):
    return messagebox.askretrycancel(title, message, parent=parent)

def open_file(parent, **options):
    return filedialog.askopenfilename(parent=parent, **options)

def save_file(parent, **options):
    return filedialog.asksaveasfilename(parent=parent, **options)

def select_directory(parent, **options):
    return filedialog.askdirectory(parent=parent, **options)