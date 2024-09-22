#!/bin/bash

# Configurări pentru backupuri

# Array cu informații despre proiecte
declare -A projects=(
    ["minloppis"]="psql json"
    ["andrada"]="sqlite json"
)

# Array cu calea către manage.py și mediu virtual pentru fiecare proiect (dacă există)
declare -A manage_paths=(
    ["minloppis"]="/home/matricks/DjangoProjects/minloppis/manage.py"
    ["andrada"]="/home/matricks/DjangoProjects/andrada/manage.py"
)

declare -A venv_paths=(
    ["minloppis"]="/home/matricks/DjangoProjects/minloppis/venv/bin/activate"
    ["andrada"]="/home/matricks/DjangoProjects/andrada/venv/bin/activate"
)

# Array cu calea către baza de date SQLite (dacă există)
declare -A sqlite_paths=(
    ["andrada"]="/home/matricks/DjangoProjects/buckets/andrada/db.sqlite3"
)
