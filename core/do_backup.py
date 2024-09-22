import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.db_utils import check_db_availability


def load_config():
    config_path = os.path.join(project_root, 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def clean_old_backups(backup_path, max_backups):
    if os.path.exists(backup_path) and os.listdir(backup_path):
        files = sorted(
            [os.path.join(backup_path, f) for f in os.listdir(backup_path)],
            key=os.path.getmtime
        )
        for old_file in files[:-max_backups]:
            os.remove(old_file)
    # Mesajul despre curățare a fost eliminat


def backup_postgresql(project, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "psql", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sql")

    try:
        subprocess.run(["pg_dump", project, "-f", backup_file], check=True)
        print(f"PostgreSQL backup completed for {project}: {os.path.basename(backup_file)}")
    except subprocess.CalledProcessError:
        print(f"PostgreSQL backup failed for {project}.")


def backup_mysql(project, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "mysql", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sql")

    try:
        subprocess.run(["mysqldump", project, "-r", backup_file], check=True)
        print(f"MySQL backup completed for {project}: {os.path.basename(backup_file)}")
    except subprocess.CalledProcessError:
        print(f"MySQL backup failed for {project}.")


def backup_sqlite(project, db_path, backup_dir, timestamp):
    backup_path = os.path.join(backup_dir, "sqlite", project)
    os.makedirs(backup_path, exist_ok=True)
    backup_file = os.path.join(backup_path, f"{project}_{timestamp}.sqlite3")

    if os.path.isfile(db_path):
        try:
            shutil.copy2(db_path, backup_file)
            print(f"SQLite backup completed for {project}: {os.path.basename(backup_file)}")
        except IOError:
            print(f"SQLite backup failed for {project}.")
    else:
        print(f"SQLite backup failed for {project}: Database file not found.")


def backup_json(project, project_config, backup_dir, timestamp):
    project_path = project_config.get('project_path', '')
    venv_path = project_config.get('venv_path', '')
    use_venv = project_config.get('use_venv', False)

    if not project_path:
        print(f"JSON backup failed for {project}: project_path not set in configuration.")
        return

    manage_path = os.path.join(project_path, 'manage.py')
    if not os.path.isfile(manage_path):
        print(f"JSON backup failed for {project}: manage.py not found at {manage_path}")
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

        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_path,
                                executable='/bin/bash')

        if result.returncode == 0:
            print(f"JSON backup completed for {project}: {os.path.basename(backup_file)}")
        else:
            print(f"JSON backup failed for {project}. Error: Command returned non-zero exit status.")
            print(f"Command error: {result.stderr}")

    except Exception as e:
        print(f"JSON backup failed for {project}. Exception: {e}")


def main():
    config = load_config()
    projects = config.get('projects', {})
    app_settings = config.get('app_settings', {})

    backup_dir = app_settings.get('backup_folder', '/home/matricks/db_backups')
    max_backups = app_settings.get('backup_instances', 4)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, (project, project_config) in enumerate(projects.items()):
        if i > 0:
            print("-" * 50)  # Linie de separare între proiecte
        print(f"Processing backup for project: {project}")

        db_types = project_config.get('db_type', '').split(',')

        for db_type in db_types:
            if db_type == 'psql':
                backup_postgresql(project, backup_dir, timestamp)
            elif db_type == 'mysql':
                backup_mysql(project, backup_dir, timestamp)
            elif db_type == 'sqlite':
                sqlite_path = project_config.get('sqlite_path', '')
                if sqlite_path:
                    backup_sqlite(project, sqlite_path, backup_dir, timestamp)
            elif db_type == 'json':
                backup_json(project, project_config, backup_dir, timestamp)

            clean_old_backups(os.path.join(backup_dir, db_type, project), max_backups)

    print("Backup process completed for all projects.")


if __name__ == "__main__":
    main()