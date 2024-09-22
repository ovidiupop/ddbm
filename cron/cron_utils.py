import os
import sys
import subprocess
from tkinter import messagebox

class CronUtils:
    @staticmethod
    def generate_cron_job(values):
        python_path = sys.executable
        do_backup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../core/do_backup.py")
        schedule = f"{values['minute']} {values['hour']} {values['day']} {values['month']} {values['weekday']}"
        return f"{schedule} {python_path} {do_backup_path}"

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