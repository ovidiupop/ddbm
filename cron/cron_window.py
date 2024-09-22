import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow
from .cron_utils import CronUtils
from core.config_manager import load_config, save_config


class CronGeneratorWindow(BaseWindow):
    def __init__(self, parent):
        self.minute = tk.StringVar(value="*")
        self.hour = tk.StringVar(value="*")
        self.day = tk.StringVar(value="*")
        self.month = tk.StringVar(value="*")
        self.weekday = tk.StringVar(value="*")
        self.utils = CronUtils()
        super().__init__(parent, "Cron Job Generator")
        self.load_config()

    def create_widgets(self):
        self.create_schedule_section()
        self.create_result_section()
        self.create_button_frame()

    def create_schedule_section(self):
        schedule_frame = self.create_labeled_frame(self.main_frame, "Schedule")
        schedule_frame.columnconfigure(tuple(range(5)), weight=1)

        fields = [
            ("Minute", self.minute, ["*"] + list(range(60))),
            ("Hour", self.hour, ["*"] + list(range(24))),
            ("Day", self.day, ["*"] + list(range(1, 32))),
            ("Month", self.month, ["*"] + list(range(1, 13))),
            ("Weekday", self.weekday, ["*"] + list(range(7)))
        ]

        for i, (label, _, _) in enumerate(fields):
            ttk.Label(schedule_frame, text=label).grid(row=0, column=i, padx=5, pady=(0, 5))

        self.combos = []
        for i, (_, var, values) in enumerate(fields):
            combo = ttk.Combobox(schedule_frame, textvariable=var, values=values, width=8)
            combo.grid(row=1, column=i, padx=5)
            combo.bind("<<ComboboxSelected>>", self.on_combo_change)
            self.combos.append(combo)

    def create_result_section(self):
        result_frame = self.create_labeled_frame(self.main_frame, "Generated Cron Job")
        self.result = tk.Text(result_frame, height=2, wrap=tk.WORD)
        self.result.pack(fill=tk.X)

    def create_button_frame(self):
        button_frame, _, _ = super().create_button_frame()

        self.open_crontab_button = ttk.Button(button_frame, text="Open Crontab", command=self.open_crontab,
                                              style='Primary.TButton')
        self.open_crontab_button.grid(row=0, column=0, padx=(0, 5), sticky="w")

    def load_config(self):
        config = load_config()
        cron_settings = config.get('cron_settings', {})
        self.set_values(cron_settings)
        self.generate_cron()

    def save_config(self):
        config = load_config()
        config['cron_settings'] = self.get_values()
        save_config(config)

    def generate_cron(self):
        current_values = self.get_values()
        current_cron_job = self.utils.generate_cron_job(current_values)
        self.set_result(current_cron_job)

    def open_crontab(self):
        self.utils.open_crontab(self.top)

    def on_combo_change(self, event):
        self.save_config()
        self.generate_cron()

    def get_values(self):
        return {
            'minute': self.minute.get(),
            'hour': self.hour.get(),
            'day': self.day.get(),
            'month': self.month.get(),
            'weekday': self.weekday.get()
        }

    def set_values(self, values):
        self.minute.set(values.get('minute', '*'))
        self.hour.set(values.get('hour', '*'))
        self.day.set(values.get('day', '*'))
        self.month.set(values.get('month', '*'))
        self.weekday.set(values.get('weekday', '*'))

    def get_result(self):
        return self.result.get("1.0", tk.END)

    def set_result(self, text):
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text)


def show_cron_generator(parent):
    cron_generator = CronGeneratorWindow(parent)
    cron_generator.top.wait_window()