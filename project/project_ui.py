from tkinter import ttk


class ProjectUI:
    def __init__(self, parent, project_data):
        self.parent = parent
        self.data = project_data
        self.main_frame = parent

    def create_widgets(self):
        self.create_project_section()
        self.create_db_sections()
        self.create_button_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(100):
            self.main_frame.grid_rowconfigure(i, weight=1)

    def create_project_section(self):
        frame = self.create_labeled_frame("Project Settings")
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.create_labeled_entry(frame, "Project Name:", self.data.project_name_var, 0, required=True)
        self.create_path_input(frame, "Project Path:", self.data.project_path_var, self.data.browse_project_path, 1,
                               required=True)

        ttk.Checkbutton(frame, text="Use Virtual Environment", variable=self.data.use_venv_var,
                        command=self.toggle_venv).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))

        self.venv_frame = ttk.Frame(frame)
        self.venv_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.venv_frame.columnconfigure(1, weight=1)
        self.create_path_input(self.venv_frame, "Venv Path:", self.data.venv_path_var, self.data.browse_venv_path, 0,
                               required=True)
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
        frame = self.create_labeled_frame(f"{title} Backup")
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        ttk.Checkbutton(frame, text=f"Enable {title} Backup", variable=var,
                        command=lambda: self.toggle_db_path(title, frame)).grid(row=0, column=0, columnspan=3,
                                                                                sticky="w")

        if path_var and browse_command:
            self.db_path_frame = ttk.Frame(frame)
            self.db_path_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
            self.db_path_frame.columnconfigure(1, weight=1)
            self.create_path_input(self.db_path_frame, f"{title} Database Path:", path_var, browse_command, 0,
                                   required=True)
            self.toggle_db_path(title, frame)

    def create_labeled_frame(self, title, padding="10"):
        frame = ttk.LabelFrame(self.main_frame, text=title, padding=padding)
        frame.columnconfigure(1, weight=1)
        return frame

    def create_labeled_entry(self, parent, label, var, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="e", padx=(0, 5))
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")

    def create_path_input(self, parent, label, var, command, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="e", padx=(0, 5))
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")
        ttk.Button(parent, text="Browse", command=command).grid(row=row, column=2, padx=(5, 0))




    def create_button_frame(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=100, column=0, sticky="ew", pady=(20, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        save_button = ttk.Button(button_frame, text="Save", command=self.data.save)
        save_button.grid(row=0, column=0, sticky="w")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.data.close)
        cancel_button.grid(row=0, column=1, sticky="e")

        return button_frame, save_button, cancel_button

    def toggle_venv(self):
        if self.data.use_venv_var.get():
            self.venv_frame.grid()
        else:
            self.venv_frame.grid_remove()
        self.parent.event_generate("<<AdjustWindowSize>>")

    def toggle_db_path(self, title, frame):
        if title == "SQLite":
            if self.data.sqlite_var.get():
                self.db_path_frame.grid()
            else:
                self.db_path_frame.grid_remove()
        self.parent.event_generate("<<AdjustWindowSize>>")