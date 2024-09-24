import os
import sys
import subprocess
from tkinter import messagebox
from core.config_manager import load_config


class CronUtils:
    @staticmethod
    def generate_cron_job(values):
        # Determine the executable path
        if getattr(sys, 'frozen', False):
            executable_path = sys.executable
        else:
            executable_path = sys.executable
            script_path = os.path.abspath(sys.argv[0])
            executable_path = f"{executable_path} {script_path}"

        # Load configuration and determine backup folder
        config = load_config()
        app_settings = config.get('app_settings', {})

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        default_backup_folder = os.path.join(base_path, 'backups')
        backup_folder = app_settings.get('backup_folder', default_backup_folder)

        # Ensure the backup folder exists
        os.makedirs(backup_folder, exist_ok=True)

        log_file = os.path.join(backup_folder, 'backup.log')

        # Generate the cron schedule
        schedule = f"{values['minute']} {values['hour']} {values['day']} {values['month']} {values['weekday']}"
        return f"{schedule} {executable_path} backup >> {log_file} 2>&1"

    @staticmethod
    def open_crontab(parent_window):
        try:
            # List of commands for different terminals
            terminal_commands = [
                "x-terminal-emulator -e crontab -e",
                "gnome-terminal -- crontab -e",
                "xfce4-terminal -e 'crontab -e'",
                "konsole -e crontab -e",
                "xterm -e crontab -e"
            ]

            # Try each command until one succeeds
            for command in terminal_commands:
                if CronUtils.open_terminal_command(command):
                    return

            # Display a message if no command succeeded
            messagebox.showinfo("Crontab", "Could not automatically open the crontab editor. "
                                           "Please open a terminal manually and run the command 'crontab -e'.",
                                parent=parent_window)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening crontab: {str(e)}", parent=parent_window)

    @staticmethod
    def open_terminal_command(command):
        try:
            # Execute the command, splitting the arguments
            subprocess.Popen(command.split(), shell=False)
            return True
        except:
            return False
