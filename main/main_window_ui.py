import tkinter as tk
from tkinter import ttk
from ui.ui_components import create_projects_frame, create_progress_bar


class MainWindowUI:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.projects_frame, self.project_tree = create_projects_frame(main_frame)
        self.projects_frame.grid(row=0, column=0, sticky="nsew")

    def bind_right_click(self, callback):
        self.project_tree.bind("<Button-3>", callback)
