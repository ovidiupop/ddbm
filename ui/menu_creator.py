import tkinter as tk
from PIL import Image, ImageTk
import os

from help.help_dialogs import show_info


class MenuCreator:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.icons = {}
        self.load_all_icons()
        self.create_menu()
        self.create_context_menu()
        self.context_menu_visible = False

    def load_all_icons(self):
        icon_names = ["settings", "exit", "new", "update", "delete", "backup", "cron", "help-info", "about"]
        for name in icon_names:
            self.load_icon(name)

    def load_icon(self, name):
        try:
            icon_path = os.path.join("icons", f"{name}.png")
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                image = image.resize((16, 16), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.icons[name] = photo
                return photo
            else:
                print(f"Icon file not found: {icon_path}")
                return None
        except Exception as e:
            print(f"Error loading icon {name}: {e}")
            return None

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # App
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="App", menu=app_menu, underline=0)

        app_menu.add_command(label="Settings", command=self.callbacks['open_settings'],
                             image=self.icons.get("settings"), compound='left', accelerator="Ctrl+S")
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.root.quit,
                             image=self.icons.get("exit"), compound='left', accelerator="Ctrl+Q")

        # Project
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=project_menu, underline=0)

        project_menu.add_command(label="New", command=self.callbacks['new_project'],
                                 image=self.icons.get("new"), compound='left', accelerator="Ctrl+N")
        project_menu.add_command(label="Update", command=self.callbacks['update_project'],
                                 image=self.icons.get("update"), compound='left', accelerator="Ctrl+U")
        project_menu.add_command(label="Delete", command=self.callbacks['delete_project'],
                                 image=self.icons.get("delete"), compound='left', accelerator="Ctrl+D")

        # Actions
        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Actions", menu=actions_menu, underline=0)

        actions_menu.add_command(label="Execute Backup", command=self.callbacks['execute_backup'],
                                 image=self.icons.get("backup"), compound='left', accelerator="Ctrl+B")
        actions_menu.add_command(label="Generate Cron Job", command=self.callbacks['open_cron_generator'],
                                 image=self.icons.get("cron"), compound='left', accelerator="Ctrl+G")

        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        help_menu.add_command(label="Info", command=lambda: show_info(self.root),
                              image=self.icons.get("help-info"), compound='left', accelerator="Ctrl+I")
        help_menu.add_command(label="About", command=self.callbacks['show_about'],
                              image=self.icons.get("about"), compound='left', accelerator="F1")

        # Keyboard shortcuts
        self.root.bind('<Control-s>', lambda event: self.callbacks['open_settings']())
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        self.root.bind('<Control-n>', lambda event: self.callbacks['new_project']())
        self.root.bind('<Control-u>', lambda event: self.callbacks['update_project']())
        self.root.bind('<Control-d>', lambda event: self.callbacks['delete_project']())
        self.root.bind('<Control-b>', lambda event: self.callbacks['execute_backup']())
        self.root.bind('<Control-g>', lambda event: self.callbacks['open_cron_generator']())
        self.root.bind('<Control-i>', lambda event: show_info(self.root))
        self.root.bind('<F1>', lambda event: self.callbacks['show_about']())

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Update",
                                      command=self.callbacks['update_project'],
                                      image=self.icons.get("update"),
                                      compound='left')
        self.context_menu.add_command(label="Delete",
                                      command=self.callbacks['delete_project'],
                                      image=self.icons.get("delete"),
                                      compound='left')


def create_menu(root, callbacks):
    return MenuCreator(root, callbacks)
