import tkinter as tk
from tkinter import ttk
from ui.ui_components import create_title_label, create_projects_frame, create_progress_bar
from ui.ui_components import ResultsDisplay

class MainWindowUI:
    def __init__(self, root):
        self.root = root
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        create_title_label(self.main_frame, "Database Backup Manager").pack(pady=(0, 10))

        projects_frame, self.project_tree = create_projects_frame(self.main_frame)
        projects_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.progress_bar = create_progress_bar(self.main_frame)
        self.results_display = ResultsDisplay(self.main_frame)

    def bind_right_click(self, callback):
        self.project_tree.bind("<Button-3>", callback)