import tempfile
import os
from file_utils import save_binary, read_binary, save_txt, read_txt


def test_binary_file():
    """Тест записи/чтения бинарного файла."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    try:
        test_data = b"\x00\x01\x02\x03\xFF"
        save_binary(temp_path, test_data)
        result = read_binary(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_text_file():
    """Тест записи/чтения текстового файла."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        temp_path = f.name
    try:
        test_text = "Test текст с русскими буквами"
        save_txt(temp_path, test_text)
        result = read_txt(temp_path)
        assert result == test_text
    finally:
        os.unlink(temp_path)