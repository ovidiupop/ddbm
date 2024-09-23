import tkinter as tk
from tkinter import messagebox
from core.config_manager import load_project_data, save_project_data, delete_project
from .project_window_ui import ProjectWindowUI

class ProjectWindow:
    def __init__(self, parent, project_name=None, refresh_callback=None, available_dbs=None):
        self.parent = parent
        self.project_name = project_name
        self.is_new_project = project_name is None
        self.refresh_callback = refresh_callback
        self.available_dbs = available_dbs or []

        self.initialize_variables()
        self.load_data()

        title = "New Project" if self.is_new_project else f"Update Project: {project_name}"
        self.ui = ProjectWindowUI(parent, self, title)
        self.ui.create_widgets()
        self.ui.adjust_window_size()

        self.ui.top.bind("<<AdjustWindowSize>>", lambda e: self.ui.adjust_window_size())

    def initialize_variables(self):
        self.project_name_var = tk.StringVar()
        self.project_path_var = tk.StringVar()
        self.use_venv_var = tk.BooleanVar(value=False)
        self.venv_path_var = tk.StringVar()
        self.psql_var = tk.BooleanVar(value=False)
        self.mysql_var = tk.BooleanVar(value=False)
        self.sqlite_var = tk.BooleanVar(value=False)
        self.json_var = tk.BooleanVar(value=False)
        self.sqlite_path_var = tk.StringVar()

    def load_data(self):
        if not self.is_new_project:
            db_type, venv_path, sqlite_path, project_path, use_venv = load_project_data(self.project_name)
            self.project_name_var.set(self.project_name)
            self.psql_var.set('psql' in db_type if db_type else False)
            self.mysql_var.set('mysql' in db_type if db_type else False)
            self.sqlite_var.set('sqlite' in db_type if db_type else False)
            self.json_var.set('json' in db_type if db_type else False)
            self.sqlite_path_var.set(sqlite_path)
            self.venv_path_var.set(venv_path)
            self.project_path_var.set(project_path)
            self.use_venv_var.set(use_venv)
        self.save_initial_values()

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
        self.ui.browse_file(self.sqlite_path_var, filetypes=[("SQLite Database", "*.db *.sqlite *.sqlite3")])

    def browse_venv_path(self):
        self.ui.browse_folder(self.venv_path_var)

    def browse_project_path(self):
        self.ui.browse_folder(self.project_path_var)

    def validate_inputs(self):
        if not self.project_name_var.get().strip():
            messagebox.showerror("Error", "Project name is required.", parent=self.ui.top)
            return False
        if not self.project_path_var.get().strip():
            messagebox.showerror("Error", "Project path is required.", parent=self.ui.top)
            return False
        if self.use_venv_var.get() and not self.venv_path_var.get().strip():
            messagebox.showerror("Error", "Venv path is required when using a virtual environment.", parent=self.ui.top)
            return False
        if self.sqlite_var.get() and not self.sqlite_path_var.get().strip():
            messagebox.showerror("Error", "SQLite database path is required when SQLite backup is enabled.", parent=self.ui.top)
            return False
        return True

    def save(self):
        if not self.validate_inputs():
            return

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

        action = "created" if self.is_new_project else "updated"
        messagebox.showinfo("Success", f"Project '{new_project_name}' has been {action}.", parent=self.ui.top)

        if self.refresh_callback:
            self.refresh_callback()

        self.ui.close()

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

def show_project_window(parent, project_name=None, refresh_callback=None, available_dbs=None):
    project_window = ProjectWindow(parent, project_name, refresh_callback, available_dbs)
    project_window.ui.top.wait_window()