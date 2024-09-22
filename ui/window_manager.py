class WindowManager:
    def __init__(self):
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)
        self.raise_window(window)

    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)

    def raise_window(self, window):
        window.lift()
        window.focus_force()
        for other_window in self.windows:
            if other_window != window:
                other_window.lower()

    def make_modal(self, window):
        window.transient(window.master)
        window.grab_set()
        window.focus_set()

window_manager = WindowManager()