# config_manager.py
import os
from typing import List, Dict, Optional, Tuple

PROJECTS_FILE = './projects.txt'
MANAGE_PATHS_FILE = './manage_paths.txt'
VENV_PATHS_FILE = './venv_paths.txt'
SQLITE_PATHS_FILE = './sqlite_paths.txt'
PROJECT_PATHS_FILE = './project_paths.txt'
USE_VENV_FILE = './use_venv.txt'

CONFIG_FILES = [PROJECTS_FILE, MANAGE_PATHS_FILE, VENV_PATHS_FILE, SQLITE_PATHS_FILE, PROJECT_PATHS_FILE, USE_VENV_FILE]

def get_project_db_type(project_name: str) -> str:
    return _read_from_file(PROJECTS_FILE, project_name)

def get_project_data(project_name: str) -> Tuple[str, str]:
    db_type = _read_from_file(PROJECTS_FILE, project_name)
    project_path = _read_from_file(PROJECT_PATHS_FILE, project_name)
    return db_type, project_path

def delete_project(project_name: str) -> bool:
    project_found = False
    for file_path in CONFIG_FILES:
        project_found |= _remove_project_from_file(file_path, project_name)
    return project_found

def load_project_data(project_name: str) -> Tuple[str, str, str, str, str, bool]:
    return (
        _read_from_file(PROJECTS_FILE, project_name),
        _read_from_file(MANAGE_PATHS_FILE, project_name),
        _read_from_file(VENV_PATHS_FILE, project_name),
        _read_from_file(SQLITE_PATHS_FILE, project_name),
        _read_from_file(PROJECT_PATHS_FILE, project_name),
        _read_from_file(USE_VENV_FILE, project_name).lower() == 'true'
    )

def save_project_data(project_name: str, db_type: str, manage_path: str, venv_path: str, sqlite_path: str, project_path: str, use_venv: bool) -> None:
    _write_to_file(PROJECTS_FILE, project_name, db_type)
    _write_to_file(MANAGE_PATHS_FILE, project_name, manage_path)
    _write_to_file(VENV_PATHS_FILE, project_name, venv_path)
    _write_to_file(SQLITE_PATHS_FILE, project_name, sqlite_path)
    _write_to_file(PROJECT_PATHS_FILE, project_name, project_path)
    _write_to_file(USE_VENV_FILE, project_name, str(use_venv))

def get_all_projects() -> List[str]:
    with open(PROJECTS_FILE, 'r') as file:
        return [line.split('=')[0] for line in file]

def ensure_config_files_exist() -> None:
    for file_path in CONFIG_FILES:
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

def add_new_project(project_name: str) -> bool:
    if project_name in get_all_projects():
        return False
    for file_path in CONFIG_FILES:
        with open(file_path, 'a') as file:
            file.write(f"{project_name}=\n")
    return True

def _read_from_file(file_path: str, project_name: str) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(project_name):
                return line.strip().split('=')[1]
    return ""

def _write_to_file(file_path: str, project_name: str, value: str) -> None:
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if not line.startswith(project_name):
                file.write(line)
        file.write(f"{project_name}={value}\n")

def _remove_project_from_file(file_path: str, project_name: str) -> bool:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    project_found = any(line.startswith(project_name) for line in lines)

    if project_found:
        with open(file_path, 'w') as file:
            file.writelines(line for line in lines if not line.startswith(project_name))

    return project_found
