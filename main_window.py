import tkinter as tk
from tkinter import ttk

from info_dialogs import show_about
from menu_creator import create_menu
from backup_manager import execute_backup
from project_manager import refresh_project_list, new_project, update_project, delete_project_ui
from results_display import ResultsDisplay
from widget_factory import create_title_label, create_projects_frame, create_progress_bar
from window_utils import create_toplevel, show_error
from cron_generator_window import show_cron_generator
from settings_window import show_settings_window
from window_manager import window_manager
from db_utils import check_db_availability

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Backup Manager")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.available_dbs = check_db_availability()

        self.create_widgets()
        self.menu_creator = self.create_menu()
        self.refresh_project_list()

    def create_menu(self):
        callbacks = {
            'new_project': lambda: new_project(self.root, self.refresh_project_list, self.available_dbs),
            'update_project': self.update_project,
            'delete_project': lambda: delete_project_ui(self.root, self.project_tree, self.refresh_project_list),
            'execute_backup': self.execute_backup,
            'show_about': lambda: show_about(self.root),
            'open_cron_generator': lambda: show_cron_generator(self.root),
            'open_settings': lambda: show_settings_window(self.root)
        }
        return create_menu(self.root, callbacks)

    def create_widgets(self):
        create_title_label(self.main_frame, "Database Backup Manager").pack(pady=(0, 10))

        projects_frame, self.project_tree = create_projects_frame(self.main_frame)
        projects_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.project_tree.bind("<Button-3>", self.on_right_click)

        self.progress_bar = create_progress_bar(self.main_frame)
        self.results_display = ResultsDisplay(self.main_frame)

    def on_right_click(self, event):
        item = self.project_tree.identify('item', event.x, event.y)
        if item:
            self.project_tree.selection_set(item)
            self.menu_creator.show_context_menu(event)
        else:
            self.menu_creator.hide_context_menu()

    def refresh_project_list(self):
        refresh_project_list(self.project_tree)

    def execute_backup(self):
        execute_backup(self.progress_bar, self.results_display, self.root)

    def update_project(self):
        update_project(self.root, self.project_tree, self.refresh_project_list, self.available_dbs)

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()