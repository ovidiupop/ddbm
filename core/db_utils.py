# db_utils.py

import shutil
import subprocess

def check_db_availability():
    available_dbs = []

    # Verifică PostgreSQL
    if shutil.which('psql'):
        try:
            subprocess.run(['psql', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            available_dbs.append('postgresql')
        except subprocess.CalledProcessError:
            pass

    # Verifică MySQL
    if shutil.which('mysql'):
        try:
            subprocess.run(['mysql', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            available_dbs.append('mysql')
        except subprocess.CalledProcessError:
            pass

    # SQLite este întotdeauna disponibil
    available_dbs.append('sqlite')

    # JSON este întotdeauna disponibil
    available_dbs.append('json')

    return available_dbs