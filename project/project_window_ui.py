import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow

class ProjectWindowUI(BaseWindow):
    def __init__(self, parent, project_data, title):
        self.data = project_data
        self.venv_frame = None
        self.db_frames = {}
        super().__init__(parent, title)

    def create_widgets(self):
        self.create_project_section()
        self.create_db_sections()
        self.create_button_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(100):
            self.main_frame.grid_rowconfigure(i, weight=1)

        self.top.bind("<<AdjustWindowSize>>", self.adjust_window_size)

    def create_project_section(self):
        frame = self.create_labeled_frame(self.main_frame, "Project Settings")
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.create_labeled_entry(frame, "Project Name:", self.data.project_name_var, 0, required=True)
        self.create_path_input(frame, "Project Path:", self.data.project_path_var, self.data.browse_project_path, 1, required=True)

        ttk.Checkbutton(frame, text="Use Virtual Environment", variable=self.data.use_venv_var,
                        command=self.toggle_venv).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))

        self.venv_frame = ttk.Frame(frame)
        self.venv_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.venv_frame.columnconfigure(1, weight=1)
        self.create_path_input(self.venv_frame, "Venv Path:", self.data.venv_path_var, self.data.browse_venv_path, 0, required=True)
        self.toggle_venv()

    def create_db_sections(self):
        db_configs = [
            ("PostgreSQL", self.data.psql_var),
            ("MySQL", self.data.mysql_var),
            ("SQLite", self.data.sqlite_var, self.data.sqlite_path_var, self.data.browse_sqlite_path),
            ("JSON", self.data.json_var)
        ]

        for i, config in enumerate(db_configs):
            if config[0].lower() in [db.lower() for db in self.data.available_dbs]:
                self.create_db_section(*config, row=i + 1)

    def create_db_section(self, title, var, path_var=None, browse_command=None, row=0):
        frame = self.create_labeled_frame(self.main_frame, f"{title} Backup")
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        ttk.Checkbutton(frame, text=f"Enable {title} Backup", variable=var,
                        command=lambda: self.toggle_db_path(title)).grid(row=0, column=0, columnspan=3, sticky="w")

        db_path_frame = ttk.Frame(frame)
        db_path_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        db_path_frame.columnconfigure(1, weight=1)
        if path_var and browse_command:
            self.create_path_input(db_path_frame, f"{title} Database Path:", path_var, browse_command, 0, required=True)
        self.db_frames[title] = db_path_frame
        self.toggle_db_path(title)

    def create_labeled_entry(self, parent, label, var, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="e", padx=(0, 5))
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")

    def create_path_input(self, parent, label, var, command=None, row=0, required=False):
        entry, browse_button = super().create_path_input(parent, label, var, row=row, required=required)
        if command:
            browse_button.config(command=command)
        return entry, browse_button

    def create_button_frame(self):
        buttons = [
            ("Save", self.data.save),
            ("Cancel", self.close)
        ]
        button_frame, self.buttons = super().create_button_frame(buttons)

    def toggle_venv(self):
        if self.data.use_venv_var.get():
            self.venv_frame.grid()
        else:
            self.venv_frame.grid_remove()
        self.top.event_generate("<<AdjustWindowSize>>")

    def toggle_db_path(self, title):
        if title in self.db_frames:
            var = getattr(self.data, f"{title.lower()}_var", None)
            if var and var.get():
                self.db_frames[title].grid()
            else:
                self.db_frames[title].grid_remove()
        self.top.event_generate("<<AdjustWindowSize>>")

    def adjust_window_size(self, event=None):
        self.top.update_idletasks()
        self.top.geometry('')
        self.top.minsize(self.top.winfo_width(), self.top.winfo_height())

    def create_labeled_frame(self, parent, title, padding="10"):
        frame = ttk.LabelFrame(parent, text=title, padding=padding)
        frame.columnconfigure(1, weight=1)
        return frame