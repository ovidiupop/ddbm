import json
import os

CONFIG_FILE = 'config.json'

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

def add_new_project(project_name):
    config = load_config()
    if project_name not in config['projects']:
        config['projects'][project_name] = {}
        save_config(config)
        return True
    return False

def get_cron_settings():
    config = load_config()
    return config.get('cron_settings', {})

def save_cron_settings(cron_settings):
    config = load_config()
    config['cron_settings'] = cron_settings
    save_config(config)

def get_app_settings():
    config = load_config()
    return config.get('app_settings', {})

def save_app_settings(app_settings):
    config = load_config()
    config['app_settings'] = app_settings
    save_config(config)