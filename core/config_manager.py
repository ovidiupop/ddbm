import json
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Rulează ca executabil
        return sys._MEIPASS
    else:
        # Rulează ca script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_path():
    return resource_path(os.path.join('config', 'config.json'))

def get_absolute_path():
    if getattr(sys, 'frozen', False):
        # Când rulează ca executabil, returnează calea către executabil
        return os.path.dirname(sys.executable)
    else:
        # Când rulează ca script, returnează calea absolută curentă
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = get_base_dir()
CONFIG_FILE = get_config_path()
ABSOLUTE_PATH = get_absolute_path()

def load_config():
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        return {"projects": {}, "cron_settings": {}, "app_settings": {}}
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {CONFIG_FILE} contains invalid JSON. Initializing with empty data.")
        return {"projects": {}, "cron_settings": {}, "app_settings": {}}

def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_project_data(project_name):
    config = load_config()
    project = config['projects'].get(project_name, {})
    return project.get('db_type', ''), project.get('project_path', '')

def get_all_projects():
    config = load_config()
    return list(config['projects'].keys())

def delete_project(project_name):
    config = load_config()
    if project_name in config['projects']:
        del config['projects'][project_name]
        save_config(config)
        return True
    return False

def load_project_data(project_name):
    config = load_config()
    project = config['projects'].get(project_name, {})
    return (
        project.get('db_type', ''),
        project.get('venv_path', ''),
        project.get('sqlite_path', ''),
        project.get('project_path', ''),
        project.get('use_venv', False)
    )

def save_project_data(project_name, db_type, venv_path, sqlite_path, project_path, use_venv):
    config = load_config()
    config['projects'][project_name] = {
        'db_type': db_type,
        'venv_path': venv_path,
        'sqlite_path': sqlite_path,
        'project_path': project_path,
        'use_venv': use_venv
    }
    save_config(config)

def ensure_config_exists():
    if not os.path.exists(CONFIG_FILE):
        save_config({"projects": {}, "cron_settings": {}, "app_settings": {}})

def generate_cron_path():
    return os.path.join(ABSOLUTE_PATH, 'your_script.py')

# Funcții pentru accesarea resurselor
def get_icon_path(icon_name):
    return resource_path(os.path.join('icons', icon_name))

def get_info_file_path():
    return resource_path(os.path.join('help', 'info.txt'))