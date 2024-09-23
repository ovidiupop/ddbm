import tkinter as tk
from tkinter import ttk
from ui.base_window import BaseWindow

class BackupWindowUI(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Backup Progress", resizable=True)
        self.create_widgets()

    def create_widgets(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.status_label = ttk.Label(self.main_frame, text="Backup in progress...")
        self.status_label.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.progress_bar = ttk.Progressbar(self.main_frame, mode='indeterminate', length=300)
        self.progress_bar.grid(row=1, column=0, sticky="ew")

        self.results_text = tk.Text(self.main_frame, wrap=tk.WORD, height=20)  # Aproximativ 400 pixeli înălțime
        self.results_text.grid(row=1, column=0, sticky="nsew")
        self.results_text.grid_remove()

        # Adăugăm un scrollbar pentru results_text
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.results_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.results_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid_remove()

    def start_progress(self):
        self.progress_bar.start(10)

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()

    def show_results(self, text):
        self.status_label.config(text="Backup completed")
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, text)
        self.results_text.grid()
        self.scrollbar.grid()

    def clear(self):
        self.status_label.config(text="Backup in progress...")
        self.results_text.delete('1.0', tk.END)
        self.results_text.grid_remove()
        self.scrollbar.grid_remove()
        self.progress_bar.grid()

    def adjust_window_size(self):
        width = max(500, self.top.winfo_width())
        height = max(500, self.top.winfo_height())
        self.top.geometry(f"{width}x{height}")