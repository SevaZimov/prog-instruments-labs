import argparse
import json
from pathlib import Path
from typing import Dict, Any

from config import Config
from modes import mode_1, mode_2, mode_3


def setup_arg_parser() -> argparse.Namespace:
    """Создает и настраивает парсер аргументов командной строки.
    :return: Настроенный экземпляр ArgumentParser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'settings',
        help="Путь к JSON-файлу с настройками"
    )
    parser.add_argument(
        'mode',
        help="Режим работы программы"
    )
    return parser.parse_args()


def json_loader(path: str) -> Dict[str, Any]:
    """Загружает и проверяет JSON-файл с настройками.
    :param path: Путь к JSON-файлу конфигурации.
    :return: Словарь с загруженными настройками.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"Файл {path} не найден")

    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if 'paths' not in config:
        raise ValueError("Отсутствует секция 'paths' в конфиге")

    return config


def mode_check(mode: int) -> None:
    """Проверяет конфигурацию для выбранного режима работы.
    :param mode: Режим работы программы (1, 2 или 3)
    """
    if mode not in (1,2,3):
        raise ValueError(f"Режим программы должен соответствовать значениям 1, 2 или 3")


def main() -> None:
    """Основная функция программы."""
    args = setup_arg_parser()
    try:
        settings = json_loader(args.settings)
        mode = int(args.mode)
        mode_check(mode)
        config = Config(settings)
        match mode:
            case '1':
                mode_1(config)
            case '2':
                mode_2(config)
            case '3':
                mode_3(config)
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON-файл")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
