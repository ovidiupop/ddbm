import logging
import os

from core.config_manager import load_config


def setup_logger(log_file_path):
    logger = logging.getLogger('backup_logger')
    logger.setLevel(logging.INFO)

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def get_log_file_path():
    config = load_config()
    app_settings = config.get('app_settings', {})
    backup_folder = app_settings.get('backup_folder', '')

    if not backup_folder:
        # Fallback la un director implicit dacă backup_folder nu este setat
        backup_folder = os.path.join(os.path.dirname(__file__), '..', 'backups')

    return os.path.join(backup_folder, 'backup.log')


log_file = get_log_file_path()
logger = setup_logger(log_file)


def log_backup_operation(operation, status, details=None):
    message = f"Backup {operation} - Status: {status}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)