import tkinter as tk
from tkinter import ttk, filedialog
import os


class BaseWindow:
    def __init__(self, parent, title):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.transient(parent)
        self.top.grab_set()

        self.main_frame = ttk.Frame(self.top, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.bind_events()
        self.adjust_window_size()

    def create_widgets(self):
        pass

    def bind_events(self):
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        self.top.bind("<Escape>", lambda e: self.close())

    def close(self):
        self.top.destroy()

    def create_button_frame(self, buttons):
        """
        Creează un frame cu butoane.

        :param buttons: O listă de tupluri, fiecare tuplu conținând (text_buton, comanda_buton)
        :return: frame-ul cu butoane și un dicționar cu referințe la butoane
        """
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=100, column=0, sticky="e", pady=(20, 0))

        button_refs = {}
        for idx, (text, command) in enumerate(buttons):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=idx, padx=(0, 5) if idx < len(buttons) - 1 else 0)
            button_refs[text] = button

        return button_frame, button_refs

    def create_labeled_frame(self, parent, title, padding="10"):
        frame = ttk.LabelFrame(parent, text=title, padding=padding)
        frame.grid(sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        return frame

    def adjust_window_size(self):
        self.top.update_idletasks()
        width = self.top.winfo_reqwidth()
        height = self.top.winfo_reqheight()
        self.top.geometry(f"{width}x{height}")
        self.top.minsize(700, height)

    def create_path_input(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='e', padx=(0, 5), pady=5)
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky='ew', pady=5)
        browse_button = ttk.Button(parent, text='Browse', command=lambda: self.browse_folder(var))
        browse_button.grid(row=row, column=2, padx=(5, 0), pady=5)
        return entry, browse_button

    def browse_folder(self, var):
        current_path = var.get()
        if current_path and os.path.exists(current_path):
            initial_dir = current_path
        else:
            initial_dir = os.path.expanduser("~")
        folder = filedialog.askdirectory(parent=self.top, initialdir=initial_dir)
        if folder:
            var.set(folder)

    def save(self):
        pass

    def get_values(self):
        pass

    def set_values(self, values):
        pass
