import tkinter as tk
from ui.dialog_utils import adjust_window_size
from ui.window_manager import window_manager


class BaseWindow:
    def __init__(self, parent, title, modal=True):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.transient(parent)
        if modal:
            self.window.grab_set()

        self.create_widgets()
        self.bind_events()

        window_manager.add_window(self)

    def create_widgets(self):
        # To be implemented by subclasses
        pass

    def bind_events(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.bind("<Escape>", self.on_escape)

    def on_close(self):
        if self.confirm_close():
            window_manager.remove_window(self)
            self.window.destroy()

    def on_escape(self, event):
        self.on_close()

    def confirm_close(self):
        # To be implemented by subclasses if needed
        return True

    def adjust_size(self):
        adjust_window_size(self.window)