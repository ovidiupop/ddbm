from tkinter import messagebox


def show_info(parent, title, message):
    return messagebox.showinfo(title, message, parent=parent)


def show_error(parent, title, message):
    return messagebox.showerror(title, message, parent=parent)


def ask_yes_no(parent, title, message):
    return messagebox.askyesno(title, message, parent=parent)
