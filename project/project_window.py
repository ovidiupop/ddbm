import tkinter as tk
from tkinter import ttk
from .project_window_ui import create_project_section, create_db_sections, create_button_frame
from .project_data_manager import ProjectDataManager
from .project_window_utils import setup_window, show_info_message, on_cancel, adjust_window_size
from window_manager import window_manager

class ProjectWindow:
    def __init__(self, parent, project_name, refresh_callback=None, available_dbs=None):
        self.top = setup_window(parent, project_name)
        self.refresh_callback = refresh_callback
        self.available_dbs = available_dbs or []
        self.data_manager = ProjectDataManager(project_name)
        self.create_widgets()
        self.adjust_window_size()
        self.top.bind("<Escape>", self.on_escape)

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.top, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        create_project_section(self.main_frame, self.data_manager, self.adjust_window_size)
        create_db_sections(self.main_frame, self.data_manager, self.available_dbs, self.adjust_window_size)
        create_button_frame(self.main_frame, self.save_changes, self.on_cancel)

    def adjust_window_size(self):
        adjust_window_size(self.top, self.main_frame)

    def save_changes(self):
        if not self.data_manager.validate_inputs(self.top):
            return

        self.data_manager.save_project_data()

        action = "created" if self.data_manager.is_new_project else "updated"
        show_info_message(self.top, f"Project '{self.data_manager.get_project_name()}' has been {action}.")

        if self.refresh_callback:
            self.refresh_callback()

        self.close_window()

    def on_cancel(self):
        on_cancel(self.top, self.data_manager.data_changed(), self.close_window)

    def on_escape(self, event):
        self.on_cancel()

    def close_window(self):
        self.top.grab_release()
        window_manager.remove_window(self.top)
        self.top.destroy()

def show_project_window(root, project_name, refresh_callback=None, available_dbs=None):
    return ProjectWindow(root, project_name, refresh_callback, available_dbs)