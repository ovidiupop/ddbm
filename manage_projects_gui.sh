#!/bin/bash

# Funcție pentru adăugarea unui proiect nou
add_project() {
    add_update_project "add"
}

# Funcție pentru actualizarea unui proiect existent
update_project() {
    local project_name
    project_name=$(zenity --list --title="Select Project to Update" --text="Select a project to update" \
        --column="Project" $(cut -d '=' -f1 ./projects.txt | sort))

    if [ -z "$project_name" ]; then
        zenity --error --text="No project selected for update."
        return
    fi

    add_update_project "update" "$project_name"
}

# Funcție pentru adăugare/actualizare proiect
add_update_project() {
    local action=$1
    local project_name=$2
    local db_type
    local manage_path
    local venv_path
    local sqlite_path

    if [ "$action" == "add" ]; then
        project_name=$(zenity --entry --title="Add Project" --text="Enter project name:")
    elif [ "$action" == "update" ]; then
        if [ -z "$project_name" ]; then
            zenity --error --text="No project selected."
            return
        fi

        db_type=$(grep "^$project_name=" ./projects.txt | cut -d '=' -f2)
        manage_path=$(grep "^$project_name=" ./manage_paths.txt | cut -d '=' -f2)
        venv_path=$(grep "^$project_name=" ./venv_paths.txt | cut -d '=' -f2)
        sqlite_path=$(grep "^$project_name=" ./sqlite_paths.txt | cut -d '=' -f2)
    else
        manage_path=""
        venv_path=""
        sqlite_path=""
    fi

    local options=""
    for type in psql sqlite json; do
        if echo "$db_type" | grep -q "$type"; then
            options="$options TRUE $type"
        else
            options="$options FALSE $type"
        fi
    done

    db_type=$(zenity --list --checklist --title="Select Backup Types" --text="Choose backup types for $project_name" \
        --column="Select" --column="Type" \
        $options)

    if [ -z "$db_type" ]; then
        zenity --error --text="At least one backup type must be selected."
        return
    fi

    if echo "$db_type" | grep -q "json"; then
        manage_path=$(zenity --file-selection --title="Select manage.py for $project_name" --filename="$manage_path")
        venv_path=$(zenity --file-selection --title="Select virtual environment activate script for $project_name" --filename="$venv_path")
    fi

    if echo "$db_type" | grep -q "sqlite"; then
        sqlite_path=$(zenity --file-selection --title="Select SQLite database file for $project_name" --filename="$sqlite_path")
    fi

    if [ "$action" == "update" ]; then
        sed -i "/^$project_name=.*/d" ./projects.txt
        echo "$project_name=$db_type" >> ./projects.txt
    else
        echo "$project_name=$db_type" >> ./projects.txt
    fi

    if [ "$manage_path" != "" ]; then
        sed -i "/^$project_name=.*/d" ./manage_paths.txt
        echo "$project_name=$manage_path" >> ./manage_paths.txt
    fi

    if [ "$venv_path" != "" ]; then
        sed -i "/^$project_name=.*/d" ./venv_paths.txt
        echo "$project_name=$venv_path" >> ./venv_paths.txt
    fi

    if [ "$sqlite_path" != "" ]; then
        sed -i "/^$project_name=.*/d" ./sqlite_paths.txt
        echo "$project_name=$sqlite_path" >> ./sqlite_paths.txt
    fi

    zenity --info --text="Project $project_name has been $action."
}

# Funcție pentru afișarea listei de proiecte și butoane pentru acțiuni
show_main_window() {
    local action
    action=$(zenity --list --title="Manage Projects" --text="Choose an action" \
        --column="Action" \
        "Add" \
        "Update" \
        "Cancel" \
        --width=300 --height=200)

    case $action in
        "Add")
            add_project
            ;;
        "Update")
            update_project
            ;;
        "Cancel")
            exit 0
            ;;
        *)
            zenity --error --text="Invalid action selected."
            ;;
    esac
}

# Verificăm dacă fișierele de proiecte există, dacă nu, le creăm
[ ! -f ./projects.txt ] && touch ./projects.txt
[ ! -f ./manage_paths.txt ] && touch ./manage_paths.txt
[ ! -f ./venv_paths.txt ] && touch ./venv_paths.txt
[ ! -f ./sqlite_paths.txt ] && touch ./sqlite_paths.txt

show_main_window
