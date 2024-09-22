import tkinter as tk
from tkinter import ttk


def create_checkbox(parent, text, variable):
    """Create a checkbox with the given text and variable."""
    return ttk.Checkbutton(parent, text=text, variable=variable)


def create_path_input(parent, label_text, variable, browse_command):
    """Create a labeled input field with a browse button."""
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Entry(frame, textvariable=variable).pack(side=tk.LEFT, expand=True, fill=tk.X)
    ttk.Button(frame, text="Browse", command=browse_command).pack(side=tk.RIGHT, padx=(5, 0))
    return frame


class AutoHideScrollbar(ttk.Scrollbar):
    """A scrollbar that hides itself if it's not needed."""

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
        """Check if the scrollbar is needed and show/hide accordingly."""
        if len(self.tree.get_children()) > self.tree.cget("height"):
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.scrollbar.pack_forget()
        self.after(100, self.check_scrollbar)

    def __getattr__(self, attr):
        """Delegate unknown attributes to the treeview."""
        return getattr(self.tree, attr)
