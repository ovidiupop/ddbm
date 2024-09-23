from tkinter import messagebox
from .project_window_ui import ProjectWindowUI
from .project_utils import ProjectDataManager

class ProjectWindow:
    def __init__(self, parent, project_name, refresh_callback=None, available_dbs=None):
        self.parent = parent
        self.data_manager = ProjectDataManager(project_name)
        self.refresh_callback = refresh_callback
        self.available_dbs = available_dbs or []

        self.ui = ProjectWindowUI(parent, self.data_manager, self.save_changes, self.on_cancel)
        self.ui.set_available_dbs(self.available_dbs)
        self.ui.top.bind("<Escape>", self.on_escape)
        self.ui.top.grab_set()

    def save_changes(self):
        if not self.data_manager.validate_inputs(self.ui.top):
            return

        self.data_manager.save_project_data()

        action = "created" if self.data_manager.is_new_project else "updated"
        messagebox.showinfo("Info", f"Project '{self.data_manager.get_project_name()}' has been {action}.",
                            parent=self.ui.top)

        if self.refresh_callback:
            self.refresh_callback()

        self.close_window()

    def on_cancel(self):
        if self.data_manager.data_changed():
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Are you sure you want to close?",
                                   parent=self.ui.top):
                self.close_window()
        else:
            self.close_window()

    def on_escape(self, event):
        self.on_cancel()

    def close_window(self):
        self.ui.top.grab_release()
        self.ui.top.destroy()

def show_project_window(root, project_name, refresh_callback=None, available_dbs=None):
    project_window = ProjectWindow(root, project_name, refresh_callback, available_dbs)
    root.wait_window(project_window.ui.top)
    return project_window