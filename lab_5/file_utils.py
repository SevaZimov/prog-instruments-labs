import os
import logging

logger = logging.getLogger(__name__)

def save_binary(path: str, data: bytes) -> None:
    """
    Сохраняет binary файл
    :param data: Данные для записи
    :param path: Путь к файлу
    :return:
    """
    logger.info(f"Сохранение бинарного файла: {path} (размер: {len(data)} байт)")
    try:
        with open(path, 'wb') as f:
            f.write(data)
        logger.info(f"Файл успешно сохранен: {path}")
    except (OSError, TypeError) as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        raise IOError(f"Ошибка сохранения файла: {e}")

def read_binary(path: str) -> bytes:
    """
    Читает binary файл
    :param path: Путь к файлу
    :return:
    """
    logger.info(f"Чтение бинарного файла: {path}")
    if not os.path.exists(path):
        logger.error(f"Файл не найден: {path}")
        raise FileNotFoundError(f"Файл не найден: {path}")
    with open(path, 'rb') as f:
        return f.read()

def save_txt(path: str, content: str) -> None:
    """
    Сохраняет текстовый файл
    :param path: Путь к файлу
    :param content: Данные для записи
    :return:
    """
    logger.info(f"Сохранение текстового файла: {path}")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Текстовый файл успешно сохранен: {path}")
    except (OSError, TypeError) as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        raise IOError(f"Ошибка сохранения файла: {e}")

def read_txt(path: str) -> str:
    """
    Сохраняет текстовый файл
    :param path: Путь к файлу
    :return:
    """
    logger.info(f"Чтение текстового файла: {path}")
    if not os.path.exists(path):
        logger.error(f"Файл не найден: {path}")
        raise FileNotFoundError(f"Файл не найден: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()