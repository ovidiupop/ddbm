import shutil
import subprocess


def check_db_availability():
    available_dbs = []
    if shutil.which('psql'):
        try:
            subprocess.run(['psql', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            available_dbs.append('postgresql')
        except subprocess.CalledProcessError:
            pass

    if shutil.which('mysql'):
        try:
            subprocess.run(['mysql', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            available_dbs.append('mysql')
        except subprocess.CalledProcessError:
            pass

    available_dbs.append('sqlite')
    available_dbs.append('json')

    return available_dbs
