import json
import os
import shutil
import subprocess
from datetime import datetime

def load_config():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, 'config', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {config_path}")
        return None

def get_log_file_path(config):
    app_settings = config.get('app_settings', {})
    default_backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups')
    backup_dir = app_settings.get('backup_folder', default_backup_dir)
    return os.path.join(backup_dir, 'backup.log')

def clean_old_backups(backup_path, max_backups):
    max_backups = int(max_backups)
    if os.path.exists(backup_path):
        files = sorted(
            [os.path.join(backup_path, f) for f in os.listdir(backup_path)],
            key=os.path.getmtime,
            reverse=True
        )
        for old_file in files[max_backups:]:
            os.remove(old_file)
            yield f"Removed old backup: {old_file}"

def backup_postgresql(project, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "psql", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sql")
    try:
        subprocess.run(["pg_dump", project, "-f", backup_file], check=True)
        yield f"PostgreSQL backup completed: {os.path.basename(backup_file)}"
    except subprocess.CalledProcessError as e:
        yield f"PostgreSQL backup failed for {project}: {str(e)}"

def backup_mysql(project, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "mysql", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sql")
    try:
        subprocess.run(["mysqldump", project, "-r", backup_file], check=True)
        yield f"MySQL backup completed: {os.path.basename(backup_file)}"
    except subprocess.CalledProcessError as e:
        yield f"MySQL backup failed for {project}: {str(e)}"

def backup_sqlite(project, db_path, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "sqlite", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sqlite3")
    try:
        shutil.copy2(db_path, backup_file)
        yield f"SQLite backup completed: {os.path.basename(backup_file)}"
    except IOError as e:
        yield f"SQLite backup failed for {project}: {str(e)}"

def backup_json(project, project_config, backup_dir, timestamp):
    project_path = project_config.get('project_path', '')
    venv_path = project_config.get('venv_path', '')
    use_venv = project_config.get('use_venv', False)

    if not project_path:
        yield f"JSON backup failed for {project}: project_path not set in configuration."
        return

    manage_path = os.path.join(project_path, 'manage.py')
    if not os.path.isfile(manage_path):
        yield f"JSON backup failed for {project}: manage.py not found at {manage_path}"
        return

    backup_path = os.path.join(backup_dir, "json", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.json")

    try:
        if use_venv and venv_path:
            activate_script = os.path.join(venv_path, 'bin', 'activate')
            command = f". {activate_script} && python {manage_path} dumpdata --output {backup_file}"
        else:
            command = f"python {manage_path} dumpdata --output {backup_file}"

        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_path, executable='/bin/bash')

        if result.returncode == 0:
            yield f"JSON backup completed: {os.path.basename(backup_file)}"
        else:
            yield f"JSON backup failed for {project}. Error: {result.stderr}"

    except Exception as e:
        yield f"JSON backup failed for {project}. Exception: {str(e)}"

def perform_backup(logger=None):
    try:
        config = load_config()
        if config is None:
            yield "Failed to load configuration"
            return

        projects = config.get('projects', {})
        if not projects:
            yield "No projects found in configuration"
            return

        app_settings = config.get('app_settings', {})
        default_backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups')
        backup_dir = app_settings.get('backup_folder', default_backup_dir)
        max_backups = int(app_settings.get('backup_instances', 4))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        yield "Starting backup process"

        for project, project_config in projects.items():
            yield f"Processing backup for project: {project}"

            db_types = project_config.get('db_type', '').split(',')
            for db_type in db_types:
                if db_type == 'psql':
                    yield from backup_postgresql(project, backup_dir, timestamp)
                elif db_type == 'mysql':
                    yield from backup_mysql(project, backup_dir, timestamp)
                elif db_type == 'sqlite':
                    sqlite_path = project_config.get('sqlite_path', '')
                    if sqlite_path:
                        yield from backup_sqlite(project, sqlite_path, backup_dir, timestamp)
                elif db_type == 'json':
                    yield from backup_json(project, project_config, backup_dir, timestamp)

                yield from clean_old_backups(os.path.join(backup_dir, db_type, project), max_backups)

        yield "Backup process completed for all projects."
    except Exception as e:
        yield f"An error occurred during backup: {str(e)}"