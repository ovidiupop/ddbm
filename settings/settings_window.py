from tkinter import messagebox
from .settings_window_ui import SettingsWindowUI
from .settings_utils import load_settings, save_settings, validate_settings
import logging

logger = logging.getLogger(__name__)


class SettingsWindow:
    def __init__(self, parent):
        self.ui = SettingsWindowUI(parent, self.save)
        self.load_current_settings()

    def save(self):
        settings = self.ui.get_values()
        if validate_settings(settings):
            try:
                save_settings(settings)
                logger.info("Settings saved successfully")
                messagebox.showinfo("Success", "Settings saved successfully!",
                                    parent=self.ui.top)
                self.ui.close()
            except Exception as e:
                logger.error(f"Error saving settings: {str(e)}")
                messagebox.showerror("Error", f"An error occurred while saving settings: {str(e)}")
        else:
            logger.warning("Invalid settings attempted to be saved")
            messagebox.showerror("Error", "Invalid settings. Please check your inputs.")

    def load_current_settings(self):
        try:
            current_settings = load_settings()
            self.ui.set_values(current_settings)
            logger.info("Current settings loaded successfully")
        except Exception as e:
            logger.error(f"Error loading current settings: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading settings: {str(e)}")


def show_settings_window(parent):
    settings_window = SettingsWindow(parent)
    settings_window.ui.top.wait_window()
