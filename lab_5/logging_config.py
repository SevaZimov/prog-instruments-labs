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
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = True
    return root_logger

logger = logging.getLogger(__name__)