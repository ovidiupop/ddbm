import tkinter as tk
from tkinter import ttk
from config_manager import load_config, save_config
from window_utils import create_toplevel, show_info, show_error, select_directory, adjust_window_size

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.top = create_toplevel(parent, "Settings")

        self.backup_folder = tk.StringVar()
        self.backup_instances = tk.StringVar()

        self.create_widgets()
        self.load_settings()

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        self.top.bind("<Escape>", self.on_escape)
        adjust_window_size(self.top)

    def create_widgets(self):
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_path_section(main_frame)
        self.create_backup_section(main_frame)
        self.create_button_frame(main_frame)

    def create_path_section(self, parent):
        frame = ttk.LabelFrame(parent, text="Path Settings", padding="10")
        frame.pack(fill=tk.X, pady=(0, 10))

        frame.columnconfigure(1, weight=1)

        self.create_path_input(frame, "Backup Folder:", self.backup_folder, self.browse_backup_folder, 0, required=True)

    def create_backup_section(self, parent):
        frame = ttk.LabelFrame(parent, text='Backup Settings', padding='10')
        frame.pack(fill=tk.X, pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        self.create_labeled_entry(frame, "Backup Instances:", self.backup_instances, 0, required=True)

    def create_path_input(self, parent, label, var, command, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky='e', padx=(0, 5))
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky='ew')
        ttk.Button(parent, text='Browse', command=command).grid(row=row, column=2, padx=(5, 0))

    def create_labeled_entry(self, parent, label, var, row, required=False):
        label_text = f"{label} {'*' if required else ''}"
        ttk.Label(parent, text=label_text, width=20).grid(row=row, column=0, sticky='e', padx=(0, 5))
        ttk.Spinbox(parent, from_=1, to=100, textvariable=var, width=5).grid(row=row, column=1, sticky='w')

    def create_button_frame(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        ttk.Button(button_frame, text='Save', command=self.save_settings, style='Primary.TButton').pack(side=tk.LEFT)
        ttk.Button(button_frame, text='Cancel', command=self.on_close, style='Secondary.TButton').pack(side=tk.RIGHT)

    def browse_backup_folder(self):
        folder = select_directory(self.top)
        if folder:
            self.backup_folder.set(folder)

    def save_settings(self):
        if not self.validate_inputs():
            return

        backup_folder = self.backup_folder.get().strip()
        backup_instances = self.backup_instances.get().strip()

        config = load_config()
        config['app_settings'] = {
            'backup_folder': backup_folder,
            'backup_instances': int(backup_instances)
        }
        save_config(config)

        show_info(self.top, "Success", "Settings saved successfully.")
        self.on_close()

    def validate_inputs(self):
        if not self.backup_folder.get().strip():
            show_error(self.top, "Error", "Backup Folder cannot be empty.")
            return False
        if not self.backup_instances.get().strip():
            show_error(self.top, "Error", "Backup Instances cannot be empty.")
            return False

        try:
            backup_instances = int(self.backup_instances.get())
            if backup_instances < 1:
                raise ValueError
        except ValueError:
            show_error(self.top, "Error", "Backup Instances must be a positive integer.")
            return False

        return True

    def load_settings(self):
        config = load_config()
        app_settings = config.get('app_settings', {})
        self.backup_folder.set(app_settings.get('backup_folder', ''))
        self.backup_instances.set(str(app_settings.get('backup_instances', 5)))

    def on_close(self):
        self.top.grab_release()
        self.top.destroy()
        self.parent.focus_set()

    def on_escape(self, event):
        if self.validate_inputs():
            self.on_close()

def show_settings_window(root):
    SettingsWindow(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_settings_window(root)
    root.mainloop()