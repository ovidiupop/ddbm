import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow

class ProjectWindowUI(BaseWindow):
    def __init__(self, parent, data_manager, save_command, cancel_command):
        self.data_manager = data_manager
        self.save_command = save_command
        self.cancel_command = cancel_command
        self.available_dbs = []
        self.db_frames = {}
        super().__init__(parent, "New Project" if data_manager.is_new_project else f"Update Project: {data_manager.project_name}")

    def create_widgets(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.create_project_section()

    def set_available_dbs(self, available_dbs):
        self.available_dbs = available_dbs
        self.create_db_sections()
        self.create_button_frame()
        self.adjust_window_size()

    def create_project_section(self):
        frame = self.create_labeled_frame(self.main_frame, "Project Settings")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        self.create_labeled_entry(frame, "Project Name:", self.data_manager.project_name_var, row=0, required=True)
        self.create_path_input(frame, "Project Path:", self.data_manager.project_path_var,
                               lambda: self.browse_folder(self.data_manager.project_path_var), row=1, required=True)

        ttk.Checkbutton(frame, text="Use Virtual Environment", variable=self.data_manager.use_venv_var,
                        command=self.toggle_venv).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))

        # Creăm venv_frame direct în frame-ul principal
        self.venv_frame = ttk.Frame(frame)
        self.venv_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.venv_frame.grid_columnconfigure(1, weight=1)

        # Aplicăm create_path_input direct pe venv_frame
        self.create_path_input(self.venv_frame, "Venv Path:", self.data_manager.venv_path_var,
                               lambda: self.browse_folder(self.data_manager.venv_path_var), row=0, required=True)

        self.toggle_venv()

    def create_db_sections(self):
        db_configs = [
            ("PostgreSQL", self.data_manager.psql_var),
            ("MySQL", self.data_manager.mysql_var),
            ("SQLite", self.data_manager.sqlite_var, self.data_manager.sqlite_path_var,
             lambda: self.browse_file(self.data_manager.sqlite_path_var,
            filetypes=[("SQLite Database", "*.db *.sqlite *.sqlite3 *.db3"), ("All Files", "*.*")])),
            ("JSON", self.data_manager.json_var)
        ]

        for i, config in enumerate(db_configs):
            if config[0].lower() in [db.lower() for db in self.available_dbs]:
                self.create_db_section(*config, row=i+1)

    def create_db_section(self, title, var, path_var=None, browse_command=None, row=0):
        frame = self.create_labeled_frame(self.main_frame, f"{title} Backup")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Checkbutton(frame, text=f"Enable {title} Backup", variable=var,
                        command=lambda: self.toggle_db_path(title)).grid(row=0, column=0, columnspan=2, sticky="w")

        if path_var and browse_command:
            db_path_frame = ttk.Frame(frame)
            db_path_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))
            db_path_frame.grid_columnconfigure(1, weight=1)
            self.create_path_input(db_path_frame, f"{title} Database Path:", path_var, browse_command, 0, required=True)
            self.db_frames[title] = db_path_frame
            self.toggle_db_path(title)

    def create_button_frame(self, buttons=None):
        buttons = [
            ("Save", self.save_command),
            ("Cancel", self.cancel_command)
        ]
        super().create_button_frame(buttons)

    def toggle_venv(self):
        if self.data_manager.use_venv_var.get():
            self.venv_frame.grid()
        else:
            self.venv_frame.grid_remove()
        self.adjust_window_size()

    def toggle_db_path(self, title):
        if title in self.db_frames:
            if getattr(self.data_manager, f"{title.lower()}_var").get():
                self.db_frames[title].grid()
            else:
                self.db_frames[title].grid_remove()
        self.adjust_window_size()

    def create_labeled_entry(self, parent, label, var, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="e", padx=(0, 5), pady=2)
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew", pady=2)