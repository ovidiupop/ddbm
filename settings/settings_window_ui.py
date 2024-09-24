import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow


class SettingsWindowUI(BaseWindow):
    def __init__(self, parent, save_callback):
        self.backup_folder = tk.StringVar()
        self.backup_instances = tk.StringVar(value="5")
        self.save_callback = save_callback
        super().__init__(parent, "Settings")

    def create_widgets(self):
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.create_path_section()
        self.create_backup_section()
        self.create_button_frame()

    def create_button_frame(self, buttons=False):
        buttons = [
            ("Save", self.save_callback),
            ("Cancel", self.close)
        ]
        self.buttons_frame, self.buttons = super().create_button_frame(buttons)

    def create_path_section(self):
        frame = self.create_labeled_frame(self.main_frame, "Path Settings")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(1, weight=1)

        self.create_path_input(frame, "Backup Folder:", self.backup_folder,
                               command=lambda: self.browse_folder(self.backup_folder), row=0)

    def create_backup_section(self):
        frame = self.create_labeled_frame(self.main_frame, 'Backup Settings')
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(1, weight=1)

        self.create_labeled_entry(frame, "Backup Instances:", self.backup_instances, 0, is_spinbox=True)

    def create_labeled_entry(self, parent, label, var, row, is_spinbox=False):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='e', padx=(0, 5), pady=5)
        if is_spinbox:
            ttk.Spinbox(parent, from_=1, to=100, textvariable=var, width=5).grid(row=row, column=1, sticky='w', pady=5)
        else:
            ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky='ew', pady=5)

    def get_values(self):
        return {
            'backup_folder': self.backup_folder.get().strip(),
            'backup_instances': self.backup_instances.get().strip()
        }

    def set_values(self, settings):
        self.backup_folder.set(settings.get('backup_folder', ''))
        self.backup_instances.set(str(settings.get('backup_instances', 5)))
