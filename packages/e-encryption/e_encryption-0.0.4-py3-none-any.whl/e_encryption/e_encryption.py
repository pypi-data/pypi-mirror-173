from cryptography.fernet import Fernet
from os import environ, path
from pathlib import Path


KEY_LOCATION_ENV = 'EASY_ENCRYPTION_KEY_LOCATION'


def get_key(location_key: str = None) -> str:
    """
    Return the key to encrypt and decrypt data
    """
    location_key = location_key or environ.get(
        KEY_LOCATION_ENV,
        path.join(Path.home(), 'easy_encryption.key')
    )
    if path.exists(location_key):
        with open(location_key, 'rb') as f:
            return f.read().decode('utf-8')
    else:
        key = Fernet.generate_key()
        with open(location_key, 'wb') as f:
            f.write(key)
        return key.decode('utf-8')


class EasyEncryption:

    def __init__(self, location_key: str = None):
        self._fernet = Fernet(get_key(location_key))

    def encrypt(self, message: str) -> str:
        """
        Encrypt a message
        """
        return self._fernet.encrypt(message.encode()).decode()

    def decrypt(self, enc_msg: str) -> str:
        """
        Decrypt a message
        """
        return self._fernet.decrypt(enc_msg.encode()).decode()


def encrypt(message: str) -> str:
    """
    Encrypt a message
    """
    return EasyEncryption().encrypt(message)


def decrypt(enc_msg: str) -> str:
    """
    Decrypt a message
    """
    return EasyEncryption().decrypt(enc_msg)


if __name__ == '__main__':
    enc_msg = encrypt('Hello World!!!')
    print('Encrypt', enc_msg)
    print('Decrypt', decrypt(enc_msg))
