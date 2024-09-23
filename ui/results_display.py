# ui/results_display.py

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class ResultsDisplay(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.grid(sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_widget = ScrolledText(self, wrap=tk.WORD)
        self.text_widget.grid(row=0, column=0, sticky="nsew")

    def set_text(self, text):
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert(tk.END, text)

    def clear(self):
        self.text_widget.delete('1.0', tk.END)

    def hide(self):
        self.grid_remove()

    def show(self):
        self.grid()
