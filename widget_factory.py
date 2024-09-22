import tkinter as tk
from tkinter import ttk
from gui_components import ScrollableTreeview

def create_title_label(parent, text):
    return ttk.Label(parent, text=text, font=("Helvetica", 16))

def create_projects_frame(parent):
    frame = ttk.LabelFrame(parent, text="Projects", padding="10")
    columns = ("project", "db_type", "project_path")
    tree = ScrollableTreeview(frame, columns=columns, show="headings", selectmode="browse")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=100)

    return frame, tree

def create_progress_bar(parent):
    progress_bar = ttk.Progressbar(parent, mode='indeterminate', length=300)
    progress_bar.pack(pady=(10, 0))
    progress_bar.pack_forget()
    return progress_bar