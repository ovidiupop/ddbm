from .cron_window_ui import CronGeneratorWindowUI
from .cron_utils import CronUtils
from core.config_manager import load_config, save_config


class CronGeneratorWindow:
    def __init__(self, parent):
        self.utils = CronUtils()
        self.ui = CronGeneratorWindowUI(parent, self.on_combo_change, self.open_crontab)
        self.ui.top.transient(parent)
        self.load_config()

    def load_config(self):
        config = load_config()
        cron_settings = config.get('cron_settings', {})
        self.ui.set_values(cron_settings)
        self.generate_cron()

    def save_config(self):
        config = load_config()
        config['cron_settings'] = self.ui.get_values()
        save_config(config)

    def generate_cron(self):
        current_values = self.ui.get_values()
        current_cron_job = self.utils.generate_cron_job(current_values)
        self.ui.set_result(current_cron_job)

    def open_crontab(self):
        self.utils.open_crontab(self.ui.top)

    def on_combo_change(self, event):
        self.save_config()
        self.generate_cron()


def show_cron_generator(parent):
    cron_generator = CronGeneratorWindow(parent)
    parent.wait_window(cron_generator.ui.top)