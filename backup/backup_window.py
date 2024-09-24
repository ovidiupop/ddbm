from .backup_window_ui import BackupWindowUI
from .backup_manager import execute_backup
from .backup_core import load_config


class BackupWindow:
    def __init__(self, parent):
        self.parent = parent
        self.ui = BackupWindowUI(parent)
        self.ui.top.geometry("300x100")
        self.backup_thread = None
        self.start_backup()

    def start_backup(self):
        if self.backup_thread and self.backup_thread.is_alive():
            self.ui.update_status("Backup already in progress")
            return

        self.ui.clear()
        self.ui.start_progress()

        config = load_config()
        if config is None:
            self.on_backup_complete(None, "Failed to load configuration")
            return

        self.backup_thread = execute_backup(self.update_progress, self.on_backup_complete)

    def update_progress(self, message):
        self.ui.update_status(message)

    def on_backup_complete(self, output, error):
        self.ui.stop_progress()
        if error:
            result_text = f"Error:\n{error}"
        else:
            result_text = output

        self.ui.top.geometry("1000x600")
        self.ui.top.update_idletasks()
        self.ui.show_results(result_text)
        self.backup_thread = None


def show_backup_window(parent):
    backup_window = BackupWindow(parent)
    parent.wait_window(backup_window.ui.top)
