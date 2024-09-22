# backup_manager.py

import subprocess
import threading
import os

def execute_backup(progress_bar, results_display, root):
    progress_bar.pack(pady=(10, 0))
    progress_bar.start(10)
    results_display.hide()

    def backup_thread():
        try:
            # Construim calea absolută către do_backup.py
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core', 'do_backup.py')
            result = subprocess.run(["python3", script_path], capture_output=True, text=True, check=True)
            output = result.stdout
            error = result.stderr
        except subprocess.CalledProcessError as e:
            output = e.stdout
            error = e.stderr
        finally:
            root.after(0, lambda: finish_backup(output, error, progress_bar, results_display))

    threading.Thread(target=backup_thread, daemon=True).start()

def finish_backup(output, error, progress_bar, results_display):
    progress_bar.stop()
    progress_bar.pack_forget()
    results_display.show()

    if error:
        results_display.set_text(f"Error:\n{error}\n")
    else:
        results_display.set_text(f"Output:\n{output}\n")