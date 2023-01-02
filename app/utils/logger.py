import json
import os
from logging import Logger, config, getLogger

FOLDER_LOG = "app/app_logs"
LOGGING_CONFIG_FILE = "app/utils/loggers.json"


def create_log_folder(folder: str = FOLDER_LOG) -> None:
    """
    Создание каталога для логгера.

    :param folder:
    :return:
    """
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name: str, template: str = "default") -> Logger:
    """
    Настройки логгера.

    :param name:
    :param template:
    :return: logger.Logger
    """
    create_log_folder()
    with open(LOGGING_CONFIG_FILE, mode="r", encoding="utf-8") as log_file:
        dict_config = json.load(log_file)
        dict_config["loggers"][name] = dict_config["loggers"][template]

    config.dictConfig(dict_config)

    return getLogger(name)
