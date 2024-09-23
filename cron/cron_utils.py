import os
import sys
import subprocess
from tkinter import messagebox
from core.config_manager import load_config

class CronUtils:
    @staticmethod
    def generate_cron_job(values):
        python_path = sys.executable
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_manager_path = os.path.join(project_root, "backup_manager.py")

        config = load_config()
        app_settings = config.get('app_settings', {})
        backup_folder = app_settings.get('backup_folder', os.path.join(project_root, 'backups'))

        log_file = os.path.join(backup_folder, 'backup.log')

        schedule = f"{values['minute']} {values['hour']} {values['day']} {values['month']} {values['weekday']}"
        return f"{schedule} {python_path} {backup_manager_path} >> {log_file} 2>&1"

    @staticmethod
    def open_crontab(parent_window):
        try:
            terminal_commands = [
                "x-terminal-emulator -e crontab -e",
                "gnome-terminal -- crontab -e",
                "xfce4-terminal -e 'crontab -e'",
                "konsole -e crontab -e",
                "xterm -e crontab -e"
            ]

            for command in terminal_commands:
                if CronUtils.open_terminal_command(command):
                    return

            messagebox.showinfo("Crontab", "Could not automatically open the crontab editor. "
                                           "Please open a terminal manually and run the command 'crontab -e'.",
                                parent=parent_window)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening crontab: {str(e)}", parent=parent_window)

    @staticmethod
    def open_terminal_command(command):
        try:
            subprocess.Popen(command.split(), shell=False)
            return True
        except:
            return False