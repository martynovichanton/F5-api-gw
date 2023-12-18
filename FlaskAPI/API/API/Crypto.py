import base64
import os
import hashlib
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto:
    def __init__(self):
        self.salt = os.urandom(64)
        self.k = Fernet.generate_key()

    def hash(self, text, iterations=1):
        hash=text
        for i in range(iterations):
            hash_object=hashlib.sha512(hash.encode())
            hash=hash_object.hexdigest()
        return hash_object.hexdigest()

    def encrypt(self, key, message):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=self.salt, iterations=100000, backend=default_backend())
        k = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        f = Fernet(k)
        return f.encrypt(message.encode())

    def decrypt(self, key, message):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=self.salt, iterations=100000, backend=default_backend())
        k = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        f = Fernet(k)
        return f.decrypt(message).decode('ascii')

    def encrypt_random_key(self, message):
        f = Fernet(self.k)
        return f.encrypt(message.encode())

    def decrypt_random_key(self, message):
        f = Fernet(self.k)
        return f.decrypt(message).decode('ascii')

# crypto = Crypto()
# #encrypt the message with key hash
# hash = crypto.hash(getpass.getpass('key '), 10)
# c = crypto.encrypt(hash, getpass.getpass('message '))
# print(f"Hash: {hash}")
# print(f"Ciper: {c}")
# d = crypto.decrypt(hash, c)
# print(f"Message: {d}")

# #encrypt the message with fernet generated key
# c = crypto.encrypt_random_key(getpass.getpass('message '))
# print(f"Ciper: {c}")
# d = crypto.decrypt_random_key(c)
# print(f"Message: {d}")
