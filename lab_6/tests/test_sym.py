import pytest
from symmetric import gen_sim_key, encrypt_sim, decrypt_sim


@pytest.mark.parametrize("key_len,expected_length", [
    (128, 16),
    (192, 24),
    (256, 32),
])
def test_gen_sim_key_lengths(key_len, expected_length):
    """Тест длин ключей."""
    key = gen_sim_key(key_len)
    assert len(key) == expected_length


def test_encrypt_decrypt():
    """Простой тест шифрования/дешифрования."""
    key = gen_sim_key(128)
    text = "Hello, World!"
    encrypted = encrypt_sim(text, key)
    decrypted = decrypt_sim(encrypted, key)
    assert decrypted == text
    assert len(encrypted) > len(text)


def test_invalid_key_length():
    """Тест некорректной длины ключа."""
    with pytest.raises(ValueError):
        gen_sim_key(100)