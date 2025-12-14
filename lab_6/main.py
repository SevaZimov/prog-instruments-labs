import argparse
import json
from pathlib import Path
from typing import Dict, Any

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


def mode_setup(config: Dict[str, Any], mode: int) -> None:
    """Проверяет конфигурацию для выбранного режима работы.
    :param config: Загруженная конфигурация
    :param mode: Режим работы программы (1, 2 или 3)
    """
    match mode:
        case 1:
            required_paths = {'symmetric_key', 'public_key', 'secret_key'}
            if 'key_len' not in config:
                raise ValueError("Отсутствует параметр 'key_len'")
            if config['key_len'] not in ('128', '192', '256'):
                raise ValueError("Недопустимая длина ключа. "
                               "Допустимые значения: '128', '192', '256'")
        case 2:
            required_paths = {'symmetric_key', 'secret_key',
                            'initial_file', 'encrypted_file'}
        case 3:
            required_paths = {'symmetric_key', 'secret_key',
                            'decrypted_file', 'encrypted_file'}
            if 'key_len' not in config:
                raise ValueError("Отсутствует параметр 'key_len'")
        case _:
            raise ValueError("Режим работы программы должен быть 1, 2 или 3")

    missing_fields = required_paths - set(config['paths'].keys())
    if missing_fields:
        raise ValueError(f"Отсутствуют обязательные пути: {missing_fields}")


def main() -> None:
    """Основная функция программы."""
    args = setup_arg_parser()
    try:
        settings = json_loader(args.settings)
        mode = int(args.mode)
        mode_setup(settings, mode)
        match args.mode:
            case '1':
                mode_1(settings)
            case '2':
                mode_2(settings)
            case '3':
                mode_3(settings)
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
