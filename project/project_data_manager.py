import tkinter as tk
from tkinter import messagebox
from config_manager import load_project_data, save_project_data, delete_project
from .project_window_utils import browse_file, browse_directory

class ProjectDataManager:
    def __init__(self, project_name):
        self.project_name = project_name
        self.is_new_project = project_name is None
        self.load_data()

    def load_data(self):
        if self.is_new_project:
            self.initialize_new_project_data()
        else:
            self.load_existing_project_data()
        self.save_initial_values()

    def initialize_new_project_data(self):
        self.project_name_var = tk.StringVar()
        self.psql_var = tk.BooleanVar(value=False)
        self.mysql_var = tk.BooleanVar(value=False)
        self.sqlite_var = tk.BooleanVar(value=False)
        self.json_var = tk.BooleanVar(value=False)
        self.sqlite_path_var = tk.StringVar()
        self.venv_path_var = tk.StringVar()
        self.project_path_var = tk.StringVar()
        self.use_venv_var = tk.BooleanVar(value=False)

    def load_existing_project_data(self):
        db_type, venv_path, sqlite_path, project_path, use_venv = load_project_data(self.project_name)
        self.project_name_var = tk.StringVar(value=self.project_name)
        self.psql_var = tk.BooleanVar(value='psql' in db_type if db_type else False)
        self.mysql_var = tk.BooleanVar(value='mysql' in db_type if db_type else False)
        self.sqlite_var = tk.BooleanVar(value='sqlite' in db_type if db_type else False)
        self.json_var = tk.BooleanVar(value='json' in db_type if db_type else False)
        self.sqlite_path_var = tk.StringVar(value=sqlite_path)
        self.venv_path_var = tk.StringVar(value=venv_path)
        self.project_path_var = tk.StringVar(value=project_path)
        self.use_venv_var = tk.BooleanVar(value=use_venv)

    def save_initial_values(self):
        self.initial_values = {
            'project_name': self.project_name_var.get(),
            'psql': self.psql_var.get(),
            'mysql': self.mysql_var.get(),
            'sqlite': self.sqlite_var.get(),
            'json': self.json_var.get(),
            'sqlite_path': self.sqlite_path_var.get(),
            'venv_path': self.venv_path_var.get(),
            'project_path': self.project_path_var.get(),
            'use_venv': self.use_venv_var.get()
        }

    def browse_sqlite_path(self):
        browse_file("Select SQLite Database File", self.sqlite_path_var)

    def browse_venv_path(self):
        browse_directory("Select Virtual Environment Directory", self.venv_path_var)

    def browse_project_path(self):
        browse_directory("Select Project Directory", self.project_path_var)

    def validate_inputs(self, parent):
        if not self.project_name_var.get().strip():
            messagebox.showerror("Error", "Project name is required.", parent=parent)
            return False
        if not self.project_path_var.get().strip():
            messagebox.showerror("Error", "Project path is required.", parent=parent)
            return False
        if self.use_venv_var.get() and not self.venv_path_var.get().strip():
            messagebox.showerror("Error", "Venv path is required when using a virtual environment.", parent=parent)
            return False
        if self.sqlite_var.get() and not self.sqlite_path_var.get().strip():
            messagebox.showerror("Error", "SQLite database path is required when SQLite backup is enabled.", parent=parent)
            return False
        return True

    def save_project_data(self):
        new_project_name = self.project_name_var.get().strip()
        new_db_type = ','.join(
            db for db, var in
            [("psql", self.psql_var), ("mysql", self.mysql_var), ("sqlite", self.sqlite_var), ("json", self.json_var)]
            if var.get())

        save_project_data(new_project_name,
                          new_db_type,
                          self.venv_path_var.get(),
                          self.sqlite_path_var.get(),
                          self.project_path_var.get(),
                          self.use_venv_var.get())

        if not self.is_new_project and new_project_name != self.project_name:
            delete_project(self.project_name)

    def get_project_name(self):
        return self.project_name_var.get().strip()

    def data_changed(self):
        current_values = {
            'project_name': self.project_name_var.get(),
            'psql': self.psql_var.get(),
            'mysql': self.mysql_var.get(),
            'sqlite': self.sqlite_var.get(),
            'json': self.json_var.get(),
            'sqlite_path': self.sqlite_path_var.get(),
            'venv_path': self.venv_path_var.get(),
            'project_path': self.project_path_var.get(),
            'use_venv': self.use_venv_var.get()
        }
        return any(self.initial_values[key] != current_values[key] for key in self.initial_values)