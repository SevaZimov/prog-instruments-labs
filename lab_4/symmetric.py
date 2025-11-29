import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def gen_sim_key(key_len: int) -> bytes:
    """Генерирует симметричный ключ заданной длины.
    :param key_len: Длина ключа в битах (128, 192 или 256).
    :return: Сгенерированный ключ в виде байтов.
    """
    if key_len % 8 != 0:
        raise ValueError("Длина ключа должна быть кратна 8")
    return os.urandom(key_len // 8)


def encrypt_sim(plain_text: str, key: bytes) -> bytes:
    """Шифрует текст с использованием AES-CBC.
    :param plain_text: Текст для шифрования.
    :param key: Ключ шифрования.
    :return: Зашифрованные данные в формате IV + ciphertext.
    """
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + cipher_text


def decrypt_sim(encrypted_data: bytes, key: bytes) -> str:
    """Дешифрует данные, зашифрованные методом AES-CBC.
    :param encrypted_data: Данные в формате IV + ciphertext.
    :param key: Ключ шифрования.
    :return: Расшифрованный текст.
    """
    iv = encrypted_data[:16]
    cipher_text = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted.decode("utf-8")