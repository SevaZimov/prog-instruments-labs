import logging


logger = logging.getLogger(__name__)


class Config:
    """Класс для работы с настройками"""
    def __init__(self, settings_dict: dict):
        logger.debug(f"Создание Config из словаря: {settings_dict}")
        self.settings = settings_dict
        self.paths = settings_dict.get('paths', {})
        self.key_len = settings_dict.get('key_len')
        logger.info(f"Config инициализирован. Длина ключа: {self.key_len}")

    def get_path(self, key: str) -> str:
        """
        Безопасное получение пути
        :param key: Имя поля для получения пути
        :return:
        """
        logger.debug(f"Запрос пути по ключу: '{key}'")
        path = self.paths.get(key)
        if not path:
            raise ValueError(f"Отсутствует путь: {key}")
        logger.debug(f"Найден путь: {key} -> {path}")
        return path

    def get_key_len(self) -> str:
        """Проверка наличия и значения key_len"""
        logger.debug(f"Проверка длины ключа: {self.key_len}")
        if not self.key_len:
            raise ValueError("Необходимо задать key_len")
        if self.key_len not in ('128', '192', '256'):
            raise ValueError("Недопустимая длина ключа. "
                             "Допустимые значения: '128', '192', '256'")
        logger.info(f"Длина ключа валидна: {self.key_len} бит")
        return self.key_len


