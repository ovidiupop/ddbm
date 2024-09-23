from tkinter import filedialog


def browse_file(title, var):
    path = filedialog.askopenfilename(title=title)
    if path:
        var.set(path)


def browse_directory(title, var):
    directory = filedialog.askdirectory(title=title)
    if directory:
        var.set(directory)
