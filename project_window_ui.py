import tkinter as tk
from tkinter import ttk
from project_window_utils import create_labeled_entry, create_path_input, toggle_venv, toggle_db_path

def create_project_section(parent, data_manager, adjust_window_size):
    frame = ttk.LabelFrame(parent, text="Project Settings", padding="10")
    frame.pack(fill=tk.X, pady=(0, 10))
    frame.columnconfigure(1, weight=1)

    create_labeled_entry(frame, "Project Name:", data_manager.project_name_var, 0, required=True)
    create_path_input(frame, "Project Path:", data_manager.project_path_var, data_manager.browse_project_path, 1, required=True)

    ttk.Checkbutton(frame, text="Use Virtual Environment", variable=data_manager.use_venv_var,
                    command=lambda: toggle_venv(data_manager, adjust_window_size)).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))

    data_manager.venv_frame = ttk.Frame(frame)
    data_manager.venv_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))
    data_manager.venv_frame.columnconfigure(1, weight=1)
    create_path_input(data_manager.venv_frame, "Venv Path:", data_manager.venv_path_var, data_manager.browse_venv_path, 0, required=True)
    toggle_venv(data_manager, adjust_window_size)

def create_db_sections(parent, data_manager, available_dbs, adjust_window_size):
    db_configs = [
        ("PostgreSQL", data_manager.psql_var),
        ("MySQL", data_manager.mysql_var),
        ("SQLite", data_manager.sqlite_var, data_manager.sqlite_path_var, data_manager.browse_sqlite_path),
        ("JSON", data_manager.json_var)
    ]

    for config in db_configs:
        if config[0].lower() in [db.lower() for db in available_dbs]:
            create_db_section(parent, data_manager, adjust_window_size, *config)

def create_db_section(parent, data_manager, adjust_window_size, title, var, path_var=None, browse_command=None):
    frame = ttk.LabelFrame(parent, text=f"{title} Backup", padding="10")
    frame.pack(fill=tk.X, pady=(0, 10))
    frame.columnconfigure(1, weight=1)

    ttk.Checkbutton(frame, text=f"Enable {title} Backup", variable=var,
                    command=lambda: toggle_db_path(title, frame, data_manager, adjust_window_size)).grid(row=0, column=0, columnspan=3, sticky="w")

    if path_var and browse_command:
        data_manager.db_path_frame = ttk.Frame(frame)
        data_manager.db_path_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        data_manager.db_path_frame.columnconfigure(1, weight=1)
        create_path_input(data_manager.db_path_frame, f"{title} Database Path:", path_var, browse_command, 0, required=True)
        toggle_db_path(title, frame, data_manager, adjust_window_size)

def create_button_frame(parent, save_command, cancel_command):
    button_frame = ttk.Frame(parent)
    button_frame.pack(fill=tk.X, pady=(20, 0))
    ttk.Button(button_frame, text="Save", command=save_command, style='Primary.TButton').pack(side=tk.LEFT)
    ttk.Button(button_frame, text="Cancel", command=cancel_command, style='Secondary.TButton').pack(side=tk.RIGHT)