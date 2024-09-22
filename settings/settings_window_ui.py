import tkinter as tk
from tkinter import ttk
from ui.dialog_utils import create_toplevel, select_directory, adjust_window_size

class SettingsWindowUI:
    def __init__(self, parent):
        self.top = create_toplevel(parent, "Settings")
        self.backup_folder = tk.StringVar()
        self.backup_instances = tk.StringVar()
        self.create_widgets()
        adjust_window_size(self.top)

    def create_widgets(self):
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_path_section(main_frame)
        self.create_backup_section(main_frame)
        self.create_button_frame(main_frame)

    def create_path_section(self, parent):
        frame = ttk.LabelFrame(parent, text="Path Settings", padding="10")
        frame.pack(fill=tk.X, pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        self.create_path_input(frame, "Backup Folder:", self.backup_folder, self.browse_backup_folder, 0, required=True)

    def create_backup_section(self, parent):
        frame = ttk.LabelFrame(parent, text='Backup Settings', padding='10')
        frame.pack(fill=tk.X, pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        self.create_labeled_entry(frame, "Backup Instances:", self.backup_instances, 0, required=True)

    def create_path_input(self, parent, label, var, command, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky='e', padx=(0, 5))
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky='ew')
        ttk.Button(parent, text='Browse', command=command).grid(row=row, column=2, padx=(5, 0))

    def create_labeled_entry(self, parent, label, var, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky='e', padx=(0, 5))
        ttk.Spinbox(parent, from_=1, to=100, textvariable=var, width=5).grid(row=row, column=1, sticky='w')

    def create_button_frame(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        self.save_button = ttk.Button(button_frame, text='Save', style='Primary.TButton')
        self.save_button.pack(side=tk.LEFT)
        self.cancel_button = ttk.Button(button_frame, text='Cancel', style='Secondary.TButton')
        self.cancel_button.pack(side=tk.RIGHT)

    def browse_backup_folder(self):
        folder = select_directory(self.top)
        if folder:
            self.backup_folder.set(folder)

    def bind_events(self, save_callback, close_callback, escape_callback):
        self.save_button.config(command=save_callback)
        self.cancel_button.config(command=close_callback)
        self.top.protocol("WM_DELETE_WINDOW", close_callback)
        self.top.bind("<Escape>", escape_callback)

    def get_values(self):
        return {
            'backup_folder': self.backup_folder.get().strip(),
            'backup_instances': self.backup_instances.get().strip()
        }

    def set_values(self, settings):
        self.backup_folder.set(settings.get('backup_folder', ''))
        self.backup_instances.set(str(settings.get('backup_instances', 5)))