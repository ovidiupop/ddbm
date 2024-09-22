import tkinter as tk
from tkinter import ttk, scrolledtext

class AutoHideScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
        else:
            self.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Scrollbar.set(self, lo, hi)

class ScrollableTreeview(ttk.Frame):
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=columns, **kwargs)
        self.scrollbar = AutoHideScrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.after(100, self.check_scrollbar)

    def identify(self, component, x, y):
        return self.tree.identify(component, x, y)

    def bind(self, sequence=None, func=None, add=None):
        self.tree.bind(sequence, func, add)

    def unbind(self, sequence, funcid=None):
        self.tree.unbind(sequence, funcid)

    def check_scrollbar(self):
        if len(self.tree.get_children()) > self.tree.cget("height"):
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.scrollbar.pack_forget()
        self.after(100, self.check_scrollbar)

    def __getattr__(self, attr):
        return getattr(self.tree, attr)

def create_checkbox(parent, text, variable):
    return ttk.Checkbutton(parent, text=text, variable=variable)

def create_path_input(parent, label_text, variable, browse_command):
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Entry(frame, textvariable=variable).pack(side=tk.LEFT, expand=True, fill=tk.X)
    ttk.Button(frame, text="Browse", command=browse_command).pack(side=tk.RIGHT, padx=(5, 0))
    return frame

def create_title_label(parent, text):
    return ttk.Label(parent, text=text, font=("Helvetica", 16))

def create_projects_frame(parent):
    frame = ttk.LabelFrame(parent, text="Projects", padding="10")
    columns = ("project", "db_type", "project_path")
    tree = ScrollableTreeview(frame, columns=columns, show="headings", selectmode="browse")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=100)

    return frame, tree

def create_progress_bar(parent):
    progress_bar = ttk.Progressbar(parent, mode='indeterminate', length=300)
    progress_bar.pack(pady=(10, 0))
    progress_bar.pack_forget()
    return progress_bar

class ResultsDisplay:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Results", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.frame.pack_forget()

        self.paned = ttk.PanedWindow(self.frame, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.text_frame = ttk.Frame(self.paned)
        self.paned.add(self.text_frame, weight=1)

        self.output_text = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.paned, height=40)
        self.paned.add(self.button_frame)

        self.close_button = ttk.Button(self.button_frame, text="Close Results", command=self.hide)
        self.close_button.pack(pady=5)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def hide(self):
        self.frame.pack_forget()

    def set_text(self, text):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, text)