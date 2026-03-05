from pathlib import Path

import platformdirs

APP_NAME = "Cerberus"
APP_AUTHOR = "Ryan de Barros"
APP_VERSION = "1.0"

PERSISTENT_PATH = Path(platformdirs.user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR, version=APP_VERSION, ensure_exists=True)).resolve()
SETTINGS_PATH = Path(platformdirs.user_config_dir(appname=APP_NAME, appauthor=APP_AUTHOR, version=APP_VERSION, roaming=True, ensure_exists=True)).resolve()
DEFAULTS_PATH = Path('default_data').resolve()
DEFAULTS_PATH.mkdir(exist_ok=True)
