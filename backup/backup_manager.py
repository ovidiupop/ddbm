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


def execute_backup(progress_callback=None, completion_callback=None, use_thread=True):
    config = load_config()
    if config is None:
        error_message = "Failed to load configuration"
        if completion_callback:
            completion_callback(None, error_message)
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
                logger.info(message)
                if progress_callback:
                    progress_callback(message)
                output.append(message)
            if completion_callback:
                completion_callback("\n".join(output), None)
        except Exception as e:
            error_message = f"Error occurred during backup: {str(e)}"
            logger.error(error_message)
            if completion_callback:
                completion_callback(None, error_message)

    if use_thread and progress_callback:
        thread = threading.Thread(target=run_backup)
        thread.start()
        return thread
    else:
        run_backup()


if __name__ == "__main__":
    execute_backup()
