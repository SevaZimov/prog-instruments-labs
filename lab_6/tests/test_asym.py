import pytest
from asymmetric import gen_asym_keys, encrypt_key, decrypt_key

def test_gen_asym_keys():
    """Простой тест генерации ключей."""
    private, public = gen_asym_keys()
    assert private is not None
    assert public is not None


@pytest.mark.parametrize("test_data", [
    b"short",
    b"16-byte-key-12345",
    b"32-byte-long-key-for-testing-123"
])
def test_encrypt_decrypt(test_data):
    """Параметризованный тест шифрования/дешифрования."""
    private, public = gen_asym_keys()

    encrypted = encrypt_key(test_data, public)
    decrypted = decrypt_key(encrypted, private)

    assert decrypted == test_data
    assert encrypted != test_data