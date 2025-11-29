class Config:
    """Класс для работы с настройками"""
    def __init__(self, settings_dict: dict):
        self.settings = settings_dict
        self.paths = settings_dict.get('paths', {})
        self.key_len = settings_dict.get('key_len')

    def get_path(self, key: str) -> str:
        """
        Безопасное получение пути
        :param key: Имя поля для получения пути
        :return:
        """
        path = self.paths.get(key)
        if not path:
            raise ValueError(f"Отсутствует путь: {key}")
        return path

    def get_key_len(self) -> str:
        """Проверка наличия и значения key_len"""
        if not self.key_len:
            raise ValueError("Необходимо задать key_len")
        if self.key_len not in ('128', '192', '256'):
            raise ValueError("Недопустимая длина ключа. "
                             "Допустимые значения: '128', '192', '256'")
        return self.key_len


