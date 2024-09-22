import tkinter as tk

from cron.cron_generator_window import show_cron_generator
from help.help_dialogs import show_about
from project.project_manager import delete_project_ui, new_project
from settings.settings_window import show_settings_window
from .main_window_ui import MainWindowUI
from .main_utils import create_menu, refresh_project_list, execute_backup, update_project
from db_utils import check_db_availability

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Backup Manager")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        self.available_dbs = check_db_availability()

        self.ui = MainWindowUI(self.root)
        self.menu_creator = create_menu(self.root, self.create_menu_callbacks())
        self.ui.bind_right_click(self.on_right_click)
        self.refresh_project_list()

    def create_menu_callbacks(self):
        return {
            'new_project': lambda: new_project(self.root, self.refresh_project_list, self.available_dbs),
            'update_project': self.update_project,
            'delete_project': lambda: delete_project_ui(self.root, self.ui.project_tree, self.refresh_project_list),
            'execute_backup': self.execute_backup,
            'show_about': lambda: show_about(self.root),
            'open_cron_generator': lambda: show_cron_generator(self.root),
            'open_settings': lambda: show_settings_window(self.root)
        }

    def refresh_project_list(self):
        refresh_project_list(self.ui.project_tree)

    def execute_backup(self):
        execute_backup(self.ui.progress_bar, self.ui.results_display, self.root)

    def update_project(self):
        update_project(self.root, self.ui.project_tree, self.refresh_project_list, self.available_dbs)

    def on_right_click(self, event):
        item = self.ui.project_tree.identify('item', event.x, event.y)
        if item:
            self.ui.project_tree.selection_set(item)
            self.menu_creator.show_context_menu(event)
        else:
            self.menu_creator.hide_context_menu()

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()