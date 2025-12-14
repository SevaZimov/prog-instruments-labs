from unittest.mock import Mock, patch
from modes import mode_1, mode_2, mode_3


def test_mode_1():
    """Тест режима 1"""
    mock_settings = {
        'key_len': '256',
        'paths': {
            'symmetric_key': 'sym.bin',
            'public_key': 'pub.pem',
            'secret_key': 'priv.pem'
        }
    }
    with patch('modes.gen_sim_key') as mock_gen_sim, \
            patch('modes.gen_asym_keys') as mock_gen_asym, \
            patch('modes.serialize_asym_keys') as mock_serialize, \
            patch('modes.encrypt_key') as mock_encrypt, \
            patch('modes.save_binary') as mock_save:
        mock_gen_sim.return_value = b"fake_key"
        mock_private = Mock()
        mock_public = Mock()
        mock_gen_asym.return_value = (mock_private, mock_public)
        mock_serialize.return_value = (b"priv_pem", b"pub_pem")
        mock_encrypt.return_value = b"encrypted"
        mode_1(mock_settings)
        mock_gen_sim.assert_called_once_with(256)
        mock_gen_asym.assert_called_once()
        mock_encrypt.assert_called_once_with(b"fake_key", mock_public)
        assert mock_save.call_count == 3


def test_mode_2():
    """Тест режима 2"""
    mock_settings = {
        'paths': {
            'symmetric_key': 'sym.bin',
            'secret_key': 'priv.pem',
            'public_key': 'pub.pem',
            'initial_file': 'input.txt',
            'encrypted_file': 'encrypted.bin'
        }
    }
    stub_private_key = Mock()
    with patch('modes.load_asym_keys') as mock_load, \
            patch('modes.read_binary') as mock_read_binary, \
            patch('modes.decrypt_key') as mock_decrypt, \
            patch('modes.read_txt') as mock_read_txt, \
            patch('modes.encrypt_sim') as mock_encrypt, \
            patch('modes.save_binary') as mock_save:
        mock_load.return_value = (stub_private_key, Mock())
        mock_read_binary.side_effect = [
            b"encrypted_sym_key",
        ]
        mock_decrypt.return_value = b"decrypted_sym_key"
        mock_read_txt.return_value = "Test text"
        mock_encrypt.return_value = b"encrypted_data"
        mode_2(mock_settings)
        mock_load.assert_called_once()
        mock_decrypt.assert_called_once_with(b"encrypted_sym_key", stub_private_key)
        mock_encrypt.assert_called_once_with("Test text", b"decrypted_sym_key")
        mock_save.assert_called_once()


def test_mode_3():
    """Тест режима 3"""
    mock_settings = {
        'paths': {
            'symmetric_key': 'sym.bin',
            'secret_key': 'priv.pem',
            'public_key': 'pub.pem',
            'encrypted_file': 'encrypted.bin',
            'decrypted_file': 'decrypted.txt'
        }
    }
    stub_private_key = Mock()
    stub_sym_key = b"fake_symmetric_key"
    stub_encrypted_data = b"fake_encrypted_data"
    stub_decrypted_text = "Decrypted text result"
    with patch('modes.load_asym_keys') as mock_load, \
            patch('modes.read_binary') as mock_read_binary, \
            patch('modes.decrypt_key') as mock_decrypt, \
            patch('modes.decrypt_sim') as mock_decrypt_sim, \
            patch('modes.save_txt') as mock_save_txt:
        mock_load.return_value = (stub_private_key, Mock())
        mock_read_binary.side_effect = [
            b"encrypted_sym_key",
            stub_encrypted_data
        ]
        mock_decrypt.return_value = stub_sym_key
        mock_decrypt_sim.return_value = stub_decrypted_text
        mode_3(mock_settings)
        mock_load.assert_called_once_with('priv.pem', 'pub.pem')
        assert mock_read_binary.call_count == 2
        mock_read_binary.assert_any_call('sym.bin')
        mock_read_binary.assert_any_call('encrypted.bin')
        mock_decrypt.assert_called_once_with(b"encrypted_sym_key", stub_private_key)
        mock_decrypt_sim.assert_called_once_with(stub_encrypted_data, stub_sym_key)
        mock_save_txt.assert_called_once_with('decrypted.txt', stub_decrypted_text)