import tkinter as tk
from tkinter import ttk

from ui.results_display import ResultsDisplay
from ui.ui_components import create_projects_frame, create_progress_bar

class MainWindowUI:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.projects_frame, self.project_tree = create_projects_frame(main_frame)
        self.projects_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.progress_bar = create_progress_bar(main_frame)
        self.results_display = ResultsDisplay(main_frame)

    def bind_right_click(self, callback):
        self.project_tree.bind("<Button-3>", callback)