from project.project_ui import ProjectUI


def __init__(self, parent, project_name=None, refresh_callback=None, available_dbs=None):
    self.project_name = project_name
    self.is_new_project = project_name is None
    self.refresh_callback = refresh_callback
    self.available_dbs = available_dbs or []

    self.initialize_variables()

    super().__init__(parent, "New Project" if self.is_new_project else f"Update Project: {project_name}")
    self.load_data()

    self.ui = ProjectUI(self.main_frame, self)
    self.ui.create_widgets()

    self.top.bind("<<AdjustWindowSize>>", lambda e: self.adjust_window_size())