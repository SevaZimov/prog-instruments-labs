from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import (RSAPrivateKey,
                                                           RSAPublicKey)


def gen_asym_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """Генерирует пару RSA ключей (приватный и публичный).
    :return: Кортеж (приватный_ключ, публичный_ключ)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_key(sim_key: bytes, public_key: RSAPublicKey) -> bytes:
    """Шифрует симметричный ключ с использованием RSA.
    :param sim_key: Симметричный ключ для шифрования
    :param public_key: Публичный RSA ключ
    :return: Зашифрованные данные
    """
    cipher_text = public_key.encrypt(
        sim_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text


def decrypt_key(cipher_text: bytes, private_key: RSAPrivateKey) -> bytes:
    """Дешифрует данные с использованием приватного RSA ключа.
    :param cipher_text: Зашифрованные данные
    :param private_key: Приватный RSA ключ
    :return: Расшифрованные данные
    """
    decrypted_key = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key


def load_asym_keys(private_key_path: str, public_key_path: str) -> tuple:
    """Загружает RSA ключи из файлов PEM формата.
    :param private_key_path: Путь к файлу приватного ключа
    :param public_key_path: Путь к файлу публичного ключа
    :return: Кортеж (приватный_ключ, публичный_ключ)
    """
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return private_key, public_key


def serialize_asym_keys(private_key: RSAPrivateKey,
                        public_key: RSAPublicKey) -> tuple:
    """Сериализует RSA ключи в PEM формат.
    :param private_key: Приватный ключ для сериализации
    :param public_key: Публичный ключ для сериализации
    :return: Кортеж (сериализованный_приватный_ключ,
    сериализованный_публичный_ключ)
    """
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem
