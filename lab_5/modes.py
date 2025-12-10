from typing import Dict, Any

from asymmetric import gen_asym_keys, serialize_asym_keys, encrypt_key, load_asym_keys, decrypt_key
from file_utils import save_binary, read_txt, read_binary, save_txt
from symmetric import gen_sim_key, encrypt_sim, decrypt_sim
from config import Config


def mode_1(config: Config) -> None:
    """
    Запускает первый режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param config: Настройки запуска сценария
    :return:
    """
    print("\nРежим 1: Создание ключей")
    key_len = int(config.get_key_len())
    print(f"Генерация симметричного ключа {key_len} бит...")
    sim_key = gen_sim_key(key_len)
    print("Генерация асимметричных ключей RSA...")
    private_key, public_key = gen_asym_keys()
    print("Сериализация ключей...")
    private_pem, public_pem = serialize_asym_keys(private_key, public_key)
    save_binary(config.get_path('secret_key'), private_pem)
    save_binary(config.get_path('public_key'), public_pem)
    print("Шифрование симметричного ключа...")
    encrypted_sim_key = encrypt_key(sim_key, public_key)
    save_binary(config.get_path('symmetric_key'), encrypted_sim_key)
    print("Все ключи успешно сгенерированы и сохранены")




def mode_2(config: Config) -> None:
    """
    Запускает второй режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param config: Настройки запуска сценария
    :return:
    """
    print("\nРежим 2: Шифрование файла")
    private_key, public_key = load_asym_keys(
        config.get_path('secret_key'),
        config.get_path('public_key')
    )
    encrypted_sim_key = read_binary(config.get_path('symmetric_key'))
    sim_key = decrypt_key(encrypted_sim_key, private_key)
    plaintext = read_txt(config.get_path('initial_file'))
    encrypted_data = encrypt_sim(plaintext, sim_key)
    save_binary(config.get_path('encrypted_file'), encrypted_data)
    print("Файл успешно зашифрован")


def mode_3(config: Config) -> None:
    """
    Запускает третий режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param config: Настройки запуска сценария
    :return:
    """
    print("\nРежим 3: Расшифровка файла")
    private_key, _ = load_asym_keys(
        config.get_path('secret_key'),
        config.get_path('public_key')
    )
    encrypted_sim_key = read_binary(config.get_path('symmetric_key'))
    sim_key = decrypt_key(encrypted_sim_key, private_key)
    encrypted_data = read_binary(config.get_path('encrypted_file'))
    decrypted_text = decrypt_sim(encrypted_data, sim_key)
    save_txt(config.get_path('decrypted_file'), decrypted_text)
    print("Файл успешно расшифрован")
