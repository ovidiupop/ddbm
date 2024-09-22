import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def setup_window(parent, project_name):
    top = tk.Toplevel(parent)
    is_new_project = project_name is None
    top.title("New Project" if is_new_project else f"Update Project: {project_name}")
    top.transient(parent)
    top.grab_set()
    return top

def create_labeled_entry(parent, label, var, row, required=False):
    label_text = f"{label} {'*' if required else ''}"
    ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky="e", padx=(0, 5))
    ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")

def create_path_input(parent, label, var, command, row, required=False):
    label_text = f"{label} {'*' if required else ''}"
    ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky="e", padx=(0, 5))
    ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")
    if command:
        ttk.Button(parent, text="Browse", command=command).grid(row=row, column=2, padx=(5, 0))

def browse_file(title, var):
    path = filedialog.askopenfilename(title=title)
    if path:
        var.set(path)

def browse_directory(title, var):
    directory = filedialog.askdirectory(title=title)
    if directory:
        var.set(directory)

def toggle_venv(data_manager, adjust_window_size):
    if data_manager.use_venv_var.get():
        data_manager.venv_frame.grid()
    else:
        data_manager.venv_frame.grid_remove()
    adjust_window_size()

def toggle_db_path(title, frame, data_manager, adjust_window_size):
    if title == "SQLite":
        if data_manager.sqlite_var.get():
            data_manager.db_path_frame.grid()
        else:
            data_manager.db_path_frame.grid_remove()
    adjust_window_size()

def show_info_message(parent, message):
    messagebox.showinfo("Info", message, parent=parent)

def on_cancel(parent, data_changed, close_window):
    if data_changed:
        if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Are you sure you want to close?", parent=parent):
            close_window()
    else:
        close_window()

def on_escape(event):
    event.widget.master.on_cancel()

def adjust_window_size(window, main_frame):
    window.update_idletasks()
    width = main_frame.winfo_reqwidth() + 40
    height = main_frame.winfo_reqheight() + 40

    max_width = int(window.winfo_screenwidth() * 0.8)
    max_height = int(window.winfo_screenheight() * 0.8)

    width = min(width, max_width)
    height = min(height, max_height)

    window.geometry(f"{width}x{height}")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"+{x}+{y}")