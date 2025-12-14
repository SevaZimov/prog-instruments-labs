import os


def save_binary(path: str, data: bytes) -> None:
    """
    Сохраняет binary файл
    :param data: Данные для записи
    :param path: Путь к файлу
    :return:
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except (OSError, TypeError) as e:
        raise IOError(f"Ошибка сохранения файла: {e}")

def read_binary(path: str) -> bytes:
    """
    Читает binary файл
    :param path: Путь к файлу
    :return:
    """
    if not os.path.exists(path):
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
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except (OSError, TypeError) as e:
        raise IOError(f"Ошибка сохранения файла: {e}")

def read_txt(path: str) -> str:
    """
    Сохраняет текстовый файл
    :param path: Путь к файлу
    :return:
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()