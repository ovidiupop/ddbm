import tkinter as tk
from tkinter import ttk, messagebox
from cron.cron_window import show_cron_generator  # Acest import a fost actualizat
from settings.settings_window import show_settings_window
from ui.styles import apply_styles
from cron.backup_manager import execute_backup
from ui.results_display import ResultsDisplay

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DB Backups App")
        apply_styles()

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Run Backup", command=self.run_backup).pack(pady=(0, 10))

        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.results_display = ResultsDisplay(main_frame)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=lambda: show_settings_window(self.root))
        file_menu.add_command(label="Exit", command=self.root.quit)

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Cron Job Generator", command=lambda: show_cron_generator(self.root))

    def run_backup(self):
        execute_backup(self.progress_bar, self.results_display, self.root)
