import tkinter as tk
from .cron_generator_ui import CronGeneratorUI
from .cron_utils import CronUtils
from config_manager import load_config, save_config
from window_utils import create_toplevel, adjust_window_size

class CronGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.window = create_toplevel(parent, "Cron Job Generator")
        self.ui = CronGeneratorUI(self.window)
        self.utils = CronUtils()

        self.load_config()
        self.ui.bind_events(self.generate_cron_if_modified, self.open_crontab, self.on_close, self.on_escape)
        self.ui.bind_combobox_events(self.save_config)

        adjust_window_size(self.window)

    def load_config(self):
        config = load_config()
        cron_settings = config.get('cron_settings', {})
        self.ui.set_values(cron_settings)
        initial_cron_job = self.utils.generate_cron_job(self.ui.get_values())
        self.ui.set_result(initial_cron_job)

    def save_config(self):
        config = load_config()
        config['cron_settings'] = self.ui.get_values()
        save_config(config)

    def generate_cron_if_modified(self):
        current_values = self.ui.get_values()
        current_cron_job = self.utils.generate_cron_job(current_values)
        if current_cron_job.strip() != self.ui.get_result().strip():
            self.ui.set_result(current_cron_job)

    def open_crontab(self):
        self.utils.open_crontab(self.window)

    def on_close(self):
        self.window.grab_release()
        self.window.destroy()
        self.parent.focus_set()

    def on_escape(self, event):
        self.on_close()

def show_cron_generator(root):
    CronGenerator(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_cron_generator(root)
    root.mainloop()