import subprocess
import threading
import os

def execute_backup(callback):
    def backup_thread():
        try:
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core', 'do_backup.py')
            result = subprocess.run(["python3", script_path], capture_output=True, text=True, check=True)
            output = result.stdout
            error = None
        except subprocess.CalledProcessError as e:
            output = e.stdout
            error = e.stderr
        callback(output, error)

    threading.Thread(target=backup_thread, daemon=True).start()