# backup_utils.py
import subprocess
import tkinter as tk
from tkinter import ttk
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_backup_script():
    logger.info("Starting backup process")
    try:
        result = subprocess.run(['bash', 'db_backups.sh'], capture_output=True, text=True, check=True)
        logger.info("Backup completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup script failed with error: {e.stderr}")
        return f"Failed to execute backup script: {e.stderr}"
    except Exception as e:
        logger.error(f"Unexpected error during backup: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

def show_backup_results(parent, results):
    """
    Afișează rezultatele backup-ului într-o fereastră nouă.

    Args:
    parent (tk.Tk): Fereastra părinte.
    results (str): Rezultatele backup-ului de afișat.
    """
    results_window = tk.Toplevel(parent)
    results_window.title("Backup Results")
    results_window.geometry("600x400")

    main_frame = ttk.Frame(results_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    results_text = tk.Text(main_frame, wrap=tk.WORD, font=("TkDefaultFont", 10))
    results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=results_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    results_text.configure(yscrollcommand=scrollbar.set)

    results_text.insert(tk.END, results)
    results_text.configure(state="disabled")

    close_button = ttk.Button(results_window, text="Close", command=results_window.destroy)
    close_button.pack(pady=10)

    logger.info("Backup results displayed to user")
