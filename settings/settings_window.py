import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from .settings_utils import load_settings, save_settings, validate_settings
import logging

logger = logging.getLogger(__name__)

class SettingsWindowUI(BaseWindow):
    def __init__(self, parent):
        self.backup_folder = tk.StringVar()
        self.backup_instances = tk.StringVar(value="5")
        super().__init__(parent, "Settings")
        self.load_current_settings()

    def create_widgets(self):
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.create_path_section()
        self.create_backup_section()
        self.create_button_frame()

    def create_path_section(self):
        frame = self.create_labeled_frame(self.main_frame, "Path Settings")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(1, weight=1)

        self.create_path_input(frame, "Backup Folder:", self.backup_folder, 0)

    def create_backup_section(self):
        frame = self.create_labeled_frame(self.main_frame, 'Backup Settings')
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(1, weight=1)

        self.create_labeled_entry(frame, "Backup Instances:", self.backup_instances, 0, is_spinbox=True)

    def create_labeled_entry(self, parent, label, var, row, is_spinbox=False):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='e', padx=(0, 5), pady=5)
        if is_spinbox:
            ttk.Spinbox(parent, from_=1, to=100, textvariable=var, width=5).grid(row=row, column=1, sticky='w', pady=5)
        else:
            ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky='ew', pady=5)

    def save(self):
        settings = self.get_values()
        if validate_settings(settings):
            try:
                save_settings(settings)
                logger.info("Settings saved successfully")
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.close()
            except Exception as e:
                logger.error(f"Error saving settings: {str(e)}")
                messagebox.showerror("Error", f"An error occurred while saving settings: {str(e)}")
        else:
            logger.warning("Invalid settings attempted to be saved")
            messagebox.showerror("Error", "Invalid settings. Please check your inputs.")

    def get_values(self):
        return {
            'backup_folder': self.backup_folder.get().strip(),
            'backup_instances': self.backup_instances.get().strip()
        }

    def set_values(self, settings):
        self.backup_folder.set(settings.get('backup_folder', ''))
        self.backup_instances.set(str(settings.get('backup_instances', 5)))

    def load_current_settings(self):
        try:
            current_settings = load_settings()
            self.set_values(current_settings)
            logger.info("Current settings loaded successfully")
        except Exception as e:
            logger.error(f"Error loading current settings: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading settings: {str(e)}")

def show_settings_window(parent):
    settings_window = SettingsWindowUI(parent)
    settings_window.top.wait_window()