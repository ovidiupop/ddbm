import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from cron.cron_window import show_cron_generator
from settings.settings_window import show_settings_window
from ui.styles import apply_styles
from cron.backup_manager import execute_backup
from ui.results_display import ResultsDisplay
from ui.ui_components import create_projects_frame, create_progress_bar, create_title_label, create_path_input
from core.config_manager import load_config, save_config
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DB Backups App")
        apply_styles()

        self.projects = []
        self.load_projects()

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = create_title_label(main_frame, "DB Backups Manager")
        title_label.pack(pady=(0, 20))

        self.projects_frame, self.projects_tree = create_projects_frame(main_frame)
        self.projects_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.populate_projects_tree()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Button(button_frame, text="Add Project", command=self.add_project).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Remove Project", command=self.remove_project).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Run Backup", command=self.run_backup).pack(side=tk.RIGHT)

        self.progress_bar = create_progress_bar(main_frame)
        self.results_display = ResultsDisplay(main_frame)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=lambda: show_settings_window(self.root))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Cron Job Generator", command=lambda: show_cron_generator(self.root))

    def run_backup(self):
        execute_backup(self.progress_bar, self.results_display, self.root)

    def load_projects(self):
        config = load_config()
        self.projects = config.get('projects', [])

    def save_projects(self):
        config = load_config()
        config['projects'] = self.projects
        save_config(config)

    def populate_projects_tree(self):
        self.projects_tree.delete(*self.projects_tree.get_children())
        for project in self.projects:
            if isinstance(project, dict):
                name = project.get('name', 'Unknown')
                db_type = project.get('db_type', 'Unknown')
                path = project.get('path', 'Unknown')
            elif isinstance(project, str):
                parts = project.split(',')
                name = parts[0] if len(parts) > 0 else 'Unknown'
                db_type = parts[1] if len(parts) > 1 else 'Unknown'
                path = parts[2] if len(parts) > 2 else 'Unknown'
            else:
                continue

            self.projects_tree.insert('', 'end', values=(name, db_type, path))

    def add_project(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Project")
        add_window.geometry("400x200")
        add_window.transient(self.root)
        add_window.grab_set()

        ttk.Label(add_window, text="Project Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_window, text="Database Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        db_type = ttk.Combobox(add_window, values=["MySQL", "PostgreSQL"])
        db_type.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        path_var = tk.StringVar()
        path_frame = create_path_input(add_window, "Project Path:", path_var, lambda: self.browse_path(path_var))
        path_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(add_window, text="Add", command=lambda: self.save_project(name_entry.get(), db_type.get(), path_var.get(), add_window)).grid(row=3, column=0, columnspan=2, pady=10)

    def browse_path(self, path_var):
        path = filedialog.askdirectory()
        if path:
            path_var.set(path)

    def save_project(self, name, db_type, path, window):
        if name and db_type and path:
            new_project = f"{name},{db_type},{path}"
            self.projects.append(new_project)
            self.save_projects()
            self.populate_projects_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required")

    def remove_project(self):
        selected_item = self.projects_tree.selection()
        if selected_item:
            index = self.projects_tree.index(selected_item)
            del self.projects[index]
            self.save_projects()
            self.populate_projects_tree()
        else:
            messagebox.showwarning("Warning", "Please select a project to remove")