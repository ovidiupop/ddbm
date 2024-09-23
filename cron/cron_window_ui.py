import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow

class CronGeneratorWindowUI(BaseWindow):
    def __init__(self, parent, on_combo_change, open_crontab):
        self.minute = tk.StringVar(value="*")
        self.hour = tk.StringVar(value="*")
        self.day = tk.StringVar(value="*")
        self.month = tk.StringVar(value="*")
        self.weekday = tk.StringVar(value="*")
        self.on_combo_change = on_combo_change
        self.open_crontab = open_crontab
        super().__init__(parent, "Cron Job Generator")

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
        result_frame.columnconfigure(0, weight=1)

        # Creăm un container pentru text și scrollbar
        text_container = ttk.Frame(result_frame)
        text_container.grid(row=0, column=0, sticky="nsew")
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)

        # Creăm controlul text cu înălțime mărită
        self.result = tk.Text(text_container, height=4, wrap=tk.WORD)
        self.result.grid(row=0, column=0, sticky="nsew")

        # Adăugăm scrollbar vertical
        scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.result.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result.config(yscrollcommand=scrollbar.set)

        # Facem controlul text read-only
        self.result.config(state=tk.DISABLED)

    def create_button_frame(self, buttons=None):
        buttons = [
            ("Open Crontab", self.open_crontab),
            ("Cancel", self.close)
        ]
        button_frame, self.buttons = super().create_button_frame(buttons)

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
        self.result.config(state=tk.NORMAL)
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text)
        self.result.config(state=tk.DISABLED)