import tkinter as tk
from tkinter import ttk

class CronGeneratorUI:
    def __init__(self, window):
        self.window = window
        self.minute = tk.StringVar(value="*")
        self.hour = tk.StringVar(value="*")
        self.day = tk.StringVar(value="*")
        self.month = tk.StringVar(value="*")
        self.weekday = tk.StringVar(value="*")
        self.result = None
        self.create_widgets()

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

        self.combos = []
        for i, (_, var, values) in enumerate(fields):
            combo = ttk.Combobox(schedule_frame, textvariable=var, values=values, width=8)
            combo.grid(row=1, column=i, padx=5)
            self.combos.append(combo)

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

        self.generate_button = ttk.Button(left_buttons, text="Generate", style='Primary.TButton')
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))

        self.open_crontab_button = ttk.Button(left_buttons, text="Open Crontab", style='Primary.TButton')
        self.open_crontab_button.pack(side=tk.LEFT)

        self.close_button = ttk.Button(button_frame, text="Close", style='Secondary.TButton')
        self.close_button.pack(side=tk.RIGHT)

    def bind_events(self, generate_command, open_crontab_command, close_command, escape_command):
        self.generate_button.config(command=generate_command)
        self.open_crontab_button.config(command=open_crontab_command)
        self.close_button.config(command=close_command)
        self.window.bind("<Escape>", escape_command)

    def bind_combobox_events(self, callback):
        for combo in self.combos:
            combo.bind("<<ComboboxSelected>>", lambda e: callback())

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