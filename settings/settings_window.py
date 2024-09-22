from .settings_window_ui import SettingsWindowUI
from .settings_utils import load_settings, save_settings, validate_settings
from window_utils import show_info, show_error

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.ui = SettingsWindowUI(parent)
        self.load_settings()
        self.ui.bind_events(self.save_settings, self.on_close, self.on_escape)

    def load_settings(self):
        settings = load_settings()
        self.ui.set_values(settings)

    def save_settings(self):
        settings = self.ui.get_values()
        if not validate_settings(settings):
            show_error(self.ui.top, "Error", "Invalid settings. Please check your inputs.")
            return

        save_settings(settings)
        show_info(self.ui.top, "Success", "Settings saved successfully.")
        self.on_close()

    def on_close(self):
        self.ui.top.grab_release()
        self.ui.top.destroy()
        self.parent.focus_set()

    def on_escape(self, event):
        if validate_settings(self.ui.get_values()):
            self.on_close()

def show_settings_window(root):
    SettingsWindow(root)

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    show_settings_window(root)
    root.mainloop()