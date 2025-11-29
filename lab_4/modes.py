from typing import Dict, Any

from asymmetric import gen_asym_keys, serialize_asym_keys, encrypt_key, load_asym_keys, decrypt_key
from file_utils import save_binary, read_txt, read_binary, save_txt
from symmetric import gen_sim_key, encrypt_sim, decrypt_sim


def mode_1(settings: Dict[str, Any]) -> None:
    """
    Запускает первый режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param settings: Настройки запуска сценария
    :return:
    """
    print("\nРежим 1: Создание ключей")
    paths = settings['paths']
    key_len = int(settings['key_len'])
    print(f"Генерация симметричного ключа {key_len} бит...")
    sim_key = gen_sim_key(key_len)
    print("Генерация асимметричных ключей RSA...")
    private_key, public_key = gen_asym_keys()
    print("Сериализация ключей...")
    private_pem, public_pem = serialize_asym_keys(private_key, public_key)
    save_binary(paths['secret_key'], private_pem)
    save_binary(paths['public_key'], public_pem)
    print("Шифрование симметричного ключа...")
    encrypted_sim_key = encrypt_key(sim_key, public_key)
    save_binary(paths['symmetric_key'], encrypted_sim_key)
    print("Все ключи успешно сгенерированы и сохранены")




def mode_2(settings: Dict[str, Any]) -> None:
    """
    Запускает второй режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param settings: Настройки запуска сценария
    :return:
    """
    print("\nРежим 2: Шифрование файла")
    paths = settings['paths']
    private_key, public_key = load_asym_keys(paths['secret_key'], paths['public_key'])
    encrypted_sim_key = read_binary(paths['symmetric_key'])
    sim_key = decrypt_key(encrypted_sim_key, private_key)
    plaintext = read_txt(paths['initial_file'])
    encrypted_data = encrypt_sim(plaintext, sim_key)
    save_binary(paths['encrypted_file'], encrypted_data)
    print("Файл успешно зашифрован")


def mode_3(settings: Dict[str, Any]) -> None:
    """
    Запускает третий режим работы
    и выводит пользователю информацию
    о каждом этапе выполнения
    :param settings: Настройки запуска сценария
    :return:
    """
    print("\nРежим 3: Расшифровка файла")
    paths = settings['paths']
    private_key, _ = load_asym_keys(paths['secret_key'], paths['public_key'])
    encrypted_sim_key = read_binary(paths['symmetric_key'])
    sim_key = decrypt_key(encrypted_sim_key, private_key)
    encrypted_data = read_binary(paths['encrypted_file'])
    decrypted_text = decrypt_sim(encrypted_data, sim_key)
    save_txt(paths['decrypted_file'], decrypted_text)
    print("Файл успешно расшифрован")
