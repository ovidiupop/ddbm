from .backup_window_ui import BackupWindowUI
from .backup_manager import execute_backup

class BackupWindow:
    def __init__(self, parent):
        self.parent = parent
        self.ui = BackupWindowUI(parent)
        self.ui.top.geometry("600x500")  # Setăm dimensiunea inițială a ferestrei
        self.start_backup()

    def start_backup(self):
        self.ui.clear()
        self.ui.start_progress()
        execute_backup(self.on_backup_complete)

    def on_backup_complete(self, output, error):
        self.ui.stop_progress()
        if error:
            result_text = f"Error:\n{error}"
        else:
            result_text = f"Output:\n{output}"
        self.ui.show_results(result_text)

def show_backup_window(parent):
    backup_window = BackupWindow(parent)
    parent.wait_window(backup_window.ui.top)