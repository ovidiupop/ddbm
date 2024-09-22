import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from config_manager import load_config, save_config
from window_utils import create_toplevel, show_error, show_info, adjust_window_size


class CronGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.window = create_toplevel(parent, "Cron Job Generator")

        self.minute = tk.StringVar(value="*")
        self.hour = tk.StringVar(value="*")
        self.day = tk.StringVar(value="*")
        self.month = tk.StringVar(value="*")
        self.weekday = tk.StringVar(value="*")

        self.create_widgets()
        self.load_config()

        self.window.bind("<Escape>", self.on_escape)
        adjust_window_size(self.window)

    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20 20 20 0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_schedule_section(main_frame)
        self.create_result_section(main_frame)
        self.create_button_frame(main_frame)

    def create_schedule_section(self, parent):
        schedule_frame = ttk.LabelFrame(parent, text="Schedule", padding="10")
        schedule_frame.pack(fill=tk.X, pady=(0, 10))

        fields = [
            ("Minute", self.minute, ["*"] + list(range(60))),
            ("Hour", self.hour, ["*"] + list(range(24))),
            ("Day", self.day, ["*"] + list(range(1, 32))),
            ("Month", self.month, ["*"] + list(range(1, 13))),
            ("Weekday", self.weekday, ["*"] + list(range(7)))
        ]

        for i, (label, _, _) in enumerate(fields):
            ttk.Label(schedule_frame, text=label).grid(row=0, column=i, padx=5, pady=(0, 5))

        for i, (_, var, values) in enumerate(fields):
            combo = ttk.Combobox(schedule_frame, textvariable=var, values=values, width=8)
            combo.grid(row=1, column=i, padx=5)
            combo.bind("<<ComboboxSelected>>", lambda e: self.save_config())

        for i in range(5):
            schedule_frame.columnconfigure(i, weight=1)

    def create_result_section(self, parent):
        result_frame = ttk.LabelFrame(parent, text="Generated Cron Job", padding="10")
        result_frame.pack(fill=tk.X, pady=(0, 10))

        self.result = tk.Text(result_frame, height=2, wrap=tk.WORD)
        self.result.pack(fill=tk.X)

    def create_button_frame(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)

        ttk.Button(left_buttons, text="Generate", command=self.generate_cron_if_modified,
                   style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(left_buttons, text="Open Crontab", command=self.open_crontab,
                   style='Primary.TButton').pack(side=tk.LEFT)

        ttk.Button(button_frame, text="Close", command=self.on_close,
                   style='Secondary.TButton').pack(side=tk.RIGHT)

    def generate_cron_if_modified(self):
        python_path = sys.executable
        do_backup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "do_backup.py")

        current_cron_job = f"{self.minute.get()} {self.hour.get()} {self.day.get()} {self.month.get()} {self.weekday.get()} {python_path} {do_backup_path}"

        if current_cron_job.strip() != self.result.get("1.0", tk.END).strip():
            self.generate_cron(python_path, do_backup_path)

    def generate_cron(self, python_path, do_backup_path):
        schedule = f"{self.minute.get()} {self.hour.get()} {self.day.get()} {self.month.get()} {self.weekday.get()}"
        cron_job = f"{schedule} {python_path} {do_backup_path}"

        if cron_job.strip() != self.result.get("1.0", tk.END).strip():
            self.result.delete(1.0, tk.END)
            self.result.insert(tk.END, cron_job)

    def open_crontab(self):
        try:
            terminal_commands = [
                "x-terminal-emulator -e crontab -e",
                "gnome-terminal -- crontab -e",
                "xfce4-terminal -e 'crontab -e'",
                "konsole -e crontab -e",
                "xterm -e crontab -e"
            ]

            for command in terminal_commands:
                if self.open_terminal_command(command):
                    return

            show_info(self.window, "Crontab", "Nu s-a putut deschide automat editorul crontab. "
                                              "Vă rugăm să deschideți manual un terminal și să rulați comanda 'crontab -e'.")

        except Exception as e:
            show_error(self.window, "Eroare", f"A apărut o eroare la deschiderea crontab: {str(e)}")

    def open_terminal_command(self, command):
        try:
            subprocess.Popen(command.split(), shell=False)
            return True
        except:
            return False

    def load_config(self):
        config = load_config()
        cron_settings = config.get('cron_settings', {})
        self.minute.set(cron_settings.get('minute', '*'))
        self.hour.set(cron_settings.get('hour', '*'))
        self.day.set(cron_settings.get('day', '*'))
        self.month.set(cron_settings.get('month', '*'))
        self.weekday.set(cron_settings.get('weekday', '*'))

        python_path = sys.executable
        do_backup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "do_backup.py")
        initial_cron_job = f"{self.minute.get()} {self.hour.get()} {self.day.get()} {self.month.get()} {self.weekday.get()} {python_path} {do_backup_path}"

        if initial_cron_job.strip():
            self.result.delete(1.0, tk.END)
            self.result.insert(tk.END, initial_cron_job)

    def save_config(self):
        config = load_config()
        config['cron_settings'] = {
            'minute': self.minute.get(),
            'hour': self.hour.get(),
            'day': self.day.get(),
            'month': self.month.get(),
            'weekday': self.weekday.get()
        }
        save_config(config)

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