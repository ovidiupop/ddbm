import tkinter as tk
from tkinter import ttk, filedialog
import os


class BaseWindow:
    def __init__(self, parent, title, resizable=False):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.transient(parent)
        self.top.resizable(width=resizable, height=resizable)
        self.top.lift(parent)
        self.top.focus_set()

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
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=100, column=0, sticky="ew", pady=(20, 0))
        button_frame.grid_columnconfigure(0, weight=1)

        button_refs = {}
        for idx, (text, command) in enumerate(buttons):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=idx + 1, padx=(0, 5))
            button_refs[text] = button

        return button_frame, button_refs

    def create_labeled_frame(self, parent, title, padding="10"):
        frame = ttk.LabelFrame(parent, text=title, padding=padding)
        frame.grid(sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)
        return frame

    def adjust_window_size(self):
        self.top.update_idletasks()
        width = max(700, self.top.winfo_reqwidth())
        height = self.top.winfo_reqheight()
        self.top.geometry(f"{width}x{height}")
        if not self.top.resizable()[0]:
            self.top.minsize(width, height)
            self.top.maxsize(width, height)

    def create_path_input(self, parent, label, var, command=None, row=0, required=False):
        parent.grid_columnconfigure(1, weight=1)

        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky='e', padx=(0, 5), pady=5)

        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky='ew', pady=5)

        if command is None:
            command = lambda: self.browse_folder(var)

        browse_button = ttk.Button(parent, text='Browse', command=command)
        browse_button.grid(row=row, column=2, sticky='e', padx=(5, 0), pady=5)

        return entry, browse_button

    def browse_folder(self, var):
        initial_dir = var.get()
        if not os.path.isdir(initial_dir):
            initial_dir = os.path.dirname(initial_dir) if os.path.isfile(initial_dir) else os.path.expanduser("~")

        folder = filedialog.askdirectory(parent=self.top, initialdir=initial_dir)
        if folder:
            var.set(folder)

    def browse_file(self, var, filetypes=None):
        initial_dir = os.path.dirname(var.get())
        if not os.path.isdir(initial_dir):
            initial_dir = os.path.expanduser("~")

        if filetypes is None:
            filetypes = [("All Files", "*.*")]

        file = filedialog.askopenfilename(
            parent=self.top,
            initialdir=initial_dir,
            filetypes=filetypes,
            title="Select SQLite Database File"
        )
        if file:
            var.set(file)

    def save(self):
        pass

    def get_values(self):
        pass

    def set_values(self, values):
        pass
