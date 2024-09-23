import sys
import os
from backup_manager import execute_backup

if __name__ == "__main__":
    def print_progress(message):
        print(message)

    def print_completion(output, error):
        if error:
            print(f"Backup failed: {error}")
        else:
            print("Backup completed successfully")
            print(output)

    execute_backup(print_progress, print_completion, use_thread=False)