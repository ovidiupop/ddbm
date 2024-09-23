import sys
import logging
import threading
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup.backup_core import perform_backup, load_config

def setup_logger(log_file):
    logger = logging.getLogger('backup_logger')
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def execute_backup(progress_callback, completion_callback, use_thread=True):
    config = load_config()
    if config is None:
        completion_callback(None, "Failed to load configuration")
        return

    backup_dir = config.get('app_settings', {}).get('backup_folder', 'backups')
    if not os.path.isabs(backup_dir):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_dir = os.path.join(project_root, backup_dir)

    log_file = os.path.join(backup_dir, 'backup.log')
    logger = setup_logger(log_file)

    def run_backup():
        try:
            output = []
            for message in perform_backup():
                output.append(message)
                logger.info(message)
                progress_callback(message)
            completion_callback("\n".join(output), None)
        except Exception as e:
            error_message = f"Error occurred during backup: {str(e)}"
            logger.error(error_message)
            completion_callback(None, error_message)

    if use_thread:
        thread = threading.Thread(target=run_backup)
        thread.start()
        return thread
    else:
        run_backup()

if __name__ == "__main__":
    config = load_config()
    if config is None:
        print("Failed to load configuration")
        sys.exit(1)

    backup_dir = config.get('app_settings', {}).get('backup_folder', 'backups')
    if not os.path.isabs(backup_dir):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_dir = os.path.join(project_root, backup_dir)

    log_file = os.path.join(backup_dir, 'backup.log')
    logger = setup_logger(log_file)

    def print_progress(message):
        pass

    def print_completion(output, error):
        if error:
            logger.error(f"Backup failed: {error}")
        else:
            logger.info("Backup completed successfully")

    execute_backup(print_progress, print_completion, use_thread=False)