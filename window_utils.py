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


def adjust_window_size(window, padding=20):
    window.update_idletasks()

    req_width = window.winfo_reqwidth()
    req_height = window.winfo_reqheight()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    new_width = min(req_width + padding, screen_width - 100)
    new_height = min(req_height + padding, screen_height - 100)

    window.geometry(f"{new_width}x{new_height}")

    # Centrăm fereastra pe ecran
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2
    window.geometry(f"+{x}+{y}")


# Restul funcțiilor existente rămân neschimbate

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