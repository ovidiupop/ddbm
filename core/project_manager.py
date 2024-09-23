from project.project_window import show_project_window
from core.config_manager import get_all_projects, delete_project as config_delete_project, get_project_data
from core.dialog_utils import show_error, show_info, ask_yes_no


def refresh_project_list(project_tree):
    for i in project_tree.get_children():
        project_tree.delete(i)
    for project in get_all_projects():
        db_type, project_path = get_project_data(project)
        project_tree.insert("", "end", values=(project, db_type, project_path))


def new_project(root, refresh_callback, available_dbs):
    show_project_window(root, None, refresh_callback, available_dbs)


def update_project(root, project_tree, refresh_callback, available_dbs):
    selected_item = project_tree.selection()
    if selected_item:
        project_name = project_tree.item(selected_item)['values'][0]
        show_project_window(root, project_name, refresh_callback, available_dbs)
    else:
        show_error(root, "No Selection", "Please select a project to update.")


def delete_project_ui(root, project_tree, refresh_callback):
    selected_item = project_tree.selection()
    if selected_item:
        project_name = project_tree.item(selected_item)['values'][0]
        if ask_yes_no(root, "Confirm Delete", f"Are you sure you want to delete the project '{project_name}'?"):
            if config_delete_project(project_name):
                show_info(root, "Success", f"Project '{project_name}' has been deleted.")
                refresh_callback()
            else:
                show_error(root, "Error", f"Failed to delete project '{project_name}'.")
    else:
        show_error(root, "No Selection", "Please select a project to delete.")
