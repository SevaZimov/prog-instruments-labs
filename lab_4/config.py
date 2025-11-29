class Config:
    """Класс для работы с настройками"""
    def __init__(self, settings_dict: dict):
        self.settings = settings_dict
        self.paths = settings_dict.get('paths', {})
        self.key_len = settings_dict.get('key_len')

    def get_path(self, key: str) -> str:
        """Безопасное получение пути"""
        path = self.paths.get(key)
        if not path:
            raise ValueError(f"Missing path: {key}")
        return path

    def require_key_len(self) -> str:
        """Проверка наличия key_len"""
        if not self.key_len:
            raise ValueError("key_len is required")
        return self.key_len

    def check_key_length(self) -> None:
        """Проверка key_len на соответствие значениям"""
        if self.key_len not in ('128', '192', '256'):
            raise ValueError("Недопустимая длина ключа. "
                             "Допустимые значения: '128', '192', '256'")