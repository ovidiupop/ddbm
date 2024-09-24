from core.config_manager import load_config, save_config
import os


def are_settings_configured():
    settings = load_settings()
    required_settings = ['backup_folder', 'backup_instances']
    if not all(settings.get(setting) for setting in required_settings):
        return False
    return validate_settings(settings)


def load_settings():
    config = load_config()
    return config.get('app_settings', {})


def save_settings(settings):
    config = load_config()
    config['app_settings'] = settings
    save_config(config)


def validate_settings(settings):
    backup_folder = settings.get('backup_folder', '')
    backup_instances = settings.get('backup_instances', '')

    if not backup_folder or not os.path.isdir(backup_folder):
        return False

    try:
        backup_instances_int = int(backup_instances)
        if backup_instances_int < 1:
            return False
    except ValueError:
        return False

    return True
