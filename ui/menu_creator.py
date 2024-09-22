import tkinter as tk
from PIL import Image, ImageTk

from help.help_dialogs import show_info


class MenuCreator:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.icons = {}
        self.create_menu()
        self.create_context_menu()
        self.context_menu_visible = False

    def load_icon(self, name):
        try:
            image = Image.open(f"icons/{name}.png")
            image = image.resize((16, 16), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.icons[name] = photo
            return photo
        except Exception as e:
            return None

    def create_menu(self):
        if "update" not in self.icons:
            self.load_icon("update")
        if "delete" not in self.icons:
            self.load_icon("delete")

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Meniul Project
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=project_menu, underline=0)

        project_menu.add_command(label="New", command=self.callbacks['new_project'],
                                 image=self.load_icon("new"), compound='left', accelerator="Ctrl+N")
        project_menu.add_command(label="Update", command=self.callbacks['update_project'],
                                 image=self.icons["update"], compound='left', accelerator="Ctrl+U")
        project_menu.add_command(label="Delete", command=self.callbacks['delete_project'],
                                 image=self.icons["delete"], compound='left', accelerator="Ctrl+D")
        project_menu.add_separator()
        project_menu.add_command(label="Settings", command=self.callbacks['open_settings'],
                                 image=self.load_icon("settings"), compound='left', accelerator="Ctrl+S")
        project_menu.add_separator()
        project_menu.add_command(label="Exit", command=self.root.quit,
                                 image=self.load_icon("exit"), compound='left', accelerator="Ctrl+Q")

        # Meniul Actions
        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Actions", menu=actions_menu, underline=0)

        actions_menu.add_command(label="Execute Backup", command=self.callbacks['execute_backup'],
                                 image=self.load_icon("backup"), compound='left', accelerator="Ctrl+B")

        actions_menu.add_command(label="Generate Cron Job", command=self.callbacks['open_cron_generator'],
                                 image=self.load_icon("cron"), compound='left',
                                 accelerator="Ctrl+G")

        # Meniul Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        help_menu.add_command(label="Info", command=lambda: show_info(self.root),
                              image=self.load_icon("help-info"), compound='left', accelerator="Ctrl+I")
        help_menu.add_command(label="About", command=self.callbacks['show_about'],
                              image=self.load_icon("about"), compound='left', accelerator="F1")

        # Bind scurtăturile la funcțiile corespunzătoare
        self.root.bind('<Control-n>', lambda event: self.callbacks['new_project']())
        self.root.bind('<Control-u>', lambda event: self.callbacks['update_project']())
        self.root.bind('<Control-d>', lambda event: self.callbacks['delete_project']())
        self.root.bind('<Control-s>', lambda event: self.callbacks['open_settings']())
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        self.root.bind('<Control-b>', lambda event: self.callbacks['execute_backup']())
        self.root.bind('<Control-g>', lambda event: self.callbacks['open_cron_generator']())
        self.root.bind('<Control-i>', lambda event: self.show_info())
        self.root.bind('<F1>', lambda event: self.callbacks['show_about']())

        self.root.update_icon = self.icons["update"]
        self.root.delete_icon = self.icons["delete"]

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Update",
                                      command=self.callbacks['update_project'],
                                      image=self.load_icon("update"),
                                      compound='left')
        self.context_menu.add_command(label="Delete",
                                      command=self.callbacks['delete_project'],
                                      image=self.load_icon("delete"),
                                      compound='left')

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
            self.context_menu_visible = True
            self.root.bind("<Button-1>", self.hide_context_menu)
        except Exception as e:
            print(f"Error displaying context menu: {e}")

    def hide_context_menu(self, event=None):
        if self.context_menu_visible:
            self.context_menu.unpost()
            self.context_menu_visible = False
            self.root.unbind("<Button-1>")

    def close_info_window(self, window):
        window.grab_release()
        window.destroy()
        self.root.focus_set()

def create_menu(root, callbacks):
    return MenuCreator(root, callbacks)