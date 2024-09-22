#!/bin/bash

# Setăm directorul de backup
BACKUP_DIR="/home/matricks/db_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Funcție pentru a păstra doar ultimele 4 fișiere
clean_old_backups() {
    BACKUP_PATH=$1
    MAX_BACKUPS=4
    if [ "$(ls -A "$BACKUP_PATH" 2>/dev/null)" ]; then
        find "$BACKUP_PATH" -maxdepth 1 -type f -printf '%T+ %p\n' | \
        sort | head -n -"$MAX_BACKUPS" | awk '{print $2}' | xargs -r rm -f
        echo "Cleaned old backups in $BACKUP_PATH, keeping only the last $MAX_BACKUPS backups."
    fi
}

# Funcție pentru backup PostgreSQL
backup_postgresql() {
    local project=$1
    local db_name=$2
    mkdir -p "$BACKUP_DIR/psql/$project"
    pg_dump "$db_name" > "$BACKUP_DIR/psql/$project/${project}_$TIMESTAMP.sql" && \
    echo "PostgreSQL backup completed for $project: ${project}_$TIMESTAMP.sql" || \
    echo "PostgreSQL backup failed for $project."
}

# Funcție pentru backup SQLite
backup_sqlite() {
    local project=$1
    local db_path=$2
    mkdir -p "$BACKUP_DIR/sqlite/$project"
    if [ -f "$db_path" ]; then
        cp "$db_path" "$BACKUP_DIR/sqlite/$project/${project}_$TIMESTAMP.sql" && \
        echo "SQLite backup completed for $project: ${project}_$TIMESTAMP.sql" || \
        echo "SQLite backup failed for $project."
    else
        echo "SQLite backup failed for $project: Database file not found."
    fi
}

# Funcție pentru backup JSON
backup_json() {
    local project=$1
    local manage_path=$2
    local venv_path=$3
    mkdir -p "$BACKUP_DIR/json/$project"
    if [ -f "$manage_path" ]; then
        if [ -f "$venv_path" ]; then
            source "$venv_path"
        fi
        python3 "$manage_path" dumpdata > "$BACKUP_DIR/json/$project/${project}_$TIMESTAMP.json" && \
        echo "JSON backup completed for $project: ${project}_$TIMESTAMP.json" || \
        echo "JSON backup failed for $project."
    else
        echo "JSON backup failed for $project: manage.py not found."
    fi
}

# Citim configurațiile
source ./config.sh

# Loop prin proiectele definite și executăm backupul în funcție de tipurile specifice
for project in "${!projects[@]}"; do
    backup_types=${projects[$project]}

    # Verificăm dacă proiectul are nevoie de backup PostgreSQL
    if [[ $backup_types == *"psql"* ]]; then
        backup_postgresql "$project" "$project"
        clean_old_backups "$BACKUP_DIR/psql/$project"
    fi

    # Verificăm dacă proiectul are nevoie de backup SQLite
    if [[ $backup_types == *"sqlite"* ]]; then
        sqlite_path=${sqlite_paths[$project]}
        backup_sqlite "$project" "$sqlite_path"
        clean_old_backups "$BACKUP_DIR/sqlite/$project"
    fi

    # Verificăm dacă proiectul are nevoie de backup JSON
    if [[ $backup_types == *"json"* ]]; then
        manage_path=${manage_paths[$project]}
        venv_path=${venv_paths[$project]}
        backup_json "$project" "$manage_path" "$venv_path"
        clean_old_backups "$BACKUP_DIR/json/$project"
    fi
done

# Încheiere
echo "Backup process completed for all projects."
