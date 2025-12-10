import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import logging


logger = logging.getLogger(__name__)


def gen_sim_key(key_len: int) -> bytes:
    """Генерирует симметричный ключ заданной длины.
    :param key_len: Длина ключа в битах (128, 192 или 256).
    :return: Сгенерированный ключ в виде байтов.
    """
    logger.info(f"Генерация симметричного ключа: {key_len} бит")
    if key_len % 8 != 0:
        raise ValueError("Длина ключа должна быть кратна 8")
    key = os.urandom(key_len // 8)
    logger.info(f"Симметричный ключ сгенерирован: {len(key)} байт")
    return key


def encrypt_sim(plain_text: str, key: bytes) -> bytes:
    """Шифрует текст с использованием AES-CBC.
    :param plain_text: Текст для шифрования.
    :param key: Ключ шифрования.
    :return: Зашифрованные данные в формате IV + ciphertext.
    """
    logger.info(f"Шифрование текста (длина: {len(plain_text)} символов)")
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    result = iv + cipher_text
    logger.info(f"Текст зашифрован. Общий размер: {len(result)} байт")
    return result


def decrypt_sim(encrypted_data: bytes, key: bytes) -> str:
    """Дешифрует данные, зашифрованные методом AES-CBC.
    :param encrypted_data: Данные в формате IV + ciphertext.
    :param key: Ключ шифрования.
    :return: Расшифрованный текст.
    """
    logger.info(f"Дешифрование данных (размер: {len(encrypted_data)} байт)")
    iv = encrypted_data[:16]
    cipher_text = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(cipher_text) + decryptor.finalize()
    result = decrypted.decode("utf-8")
    logger.info(f"Данные дешифрованы. Текст: {len(result)} символов")
    return result