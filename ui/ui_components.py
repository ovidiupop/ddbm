from tkinter import ttk


class AutoHideScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)


class ScrollableTreeview(ttk.Frame):
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=columns, **kwargs)
        self.scrollbar = AutoHideScrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.after(100, self.check_scrollbar)

    def check_scrollbar(self):
        if len(self.tree.get_children()) > self.tree.cget("height"):
            self.scrollbar.grid()
        else:
            self.scrollbar.grid_remove()
        self.after(100, self.check_scrollbar)

    def identify(self, component, x, y):
        return self.tree.identify(component, x, y)

    def bind(self, sequence=None, func=None, add=None):
        self.tree.bind(sequence, func, add)

    def unbind(self, sequence, funcid=None):
        self.tree.unbind(sequence, funcid)

    def __getattr__(self, attr):
        return getattr(self.tree, attr)


def create_projects_frame(parent):
    frame = ttk.LabelFrame(parent, text="Projects", padding="10")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    columns = ("project", "db_type", "project_path")
    tree = ScrollableTreeview(frame, columns=columns, show="headings", selectmode="browse")
    tree.grid(row=0, column=0, sticky="nsew")

    column_titles = {
        "project": "Project Name",
        "db_type": "Export Types",
        "project_path": "Project Path"
    }
    column_widths = {
        "project": 80,
        "db_type": 80,
        "project_path": 400
    }

    for col in columns:
        tree.heading(col, text=column_titles[col])
        tree.column(col, width=column_widths[col])

    return frame, tree


def create_progress_bar(parent):
    progress_bar = ttk.Progressbar(parent, mode='indeterminate', length=300)
    progress_bar.grid(row=1, column=0, pady=(10, 0), sticky="ew")
    progress_bar.grid_remove()
    return progress_bar
