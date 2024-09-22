from core.config_manager import load_config, save_config

def load_settings():
    config = load_config()
    return config.get('app_settings', {})

def save_settings(settings):
    config = load_config()
    config['app_settings'] = settings
    save_config(config)

def validate_settings(settings):
    if not settings['backup_folder']:
        return False
    try:
        backup_instances = int(settings['backup_instances'])
        if backup_instances < 1:
            return False
    except ValueError:
        return False
    return True