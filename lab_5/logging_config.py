import logging
import sys


def setup_logging():
    """
    Настраивает логирование для всех модулей приложения.
    Должна быть вызвана до импорта других модулей.
    """
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)-8s - %(name)-20s - %(message)s',
        datefmt='%H:%M:%S'
    )
    file_handler = logging.FileHandler(
        filename='lab_logs.log',
        mode='a',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = True
    return root_logger

logger = logging.getLogger(__name__)