# main/main_window_ui.py

from tkinter import ttk

from ui.results_display import ResultsDisplay
from ui.ui_components import create_projects_frame, create_progress_bar


class MainWindowUI:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        self.projects_frame, self.project_tree = create_projects_frame(main_frame)
        self.projects_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))

        self.progress_bar = create_progress_bar(main_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.grid_remove()

        self.results_display = ResultsDisplay(main_frame)
        self.results_display.grid(row=2, column=0, sticky="nsew")
        self.results_display.hide()

    def bind_right_click(self, callback):
        self.project_tree.bind("<Button-3>", callback)