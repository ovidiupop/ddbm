import tkinter as tk
from tkinter import ttk, scrolledtext

class ResultsDisplay:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Results", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.frame.pack_forget()

        # Folosim un PanedWindow pentru a permite redimensionarea
        self.paned = ttk.PanedWindow(self.frame, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Frame pentru text
        self.text_frame = ttk.Frame(self.paned)
        self.paned.add(self.text_frame, weight=1)

        # ScrolledText widget
        self.output_text = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Frame pentru buton
        self.button_frame = ttk.Frame(self.paned, height=40)
        self.paned.add(self.button_frame)

        # Buton de închidere
        self.close_button = ttk.Button(self.button_frame, text="Close Results", command=self.hide)
        self.close_button.pack(pady=5)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def hide(self):
        self.frame.pack_forget()

    def set_text(self, text):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, text)