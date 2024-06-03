from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


class EncryptionManager:
    def __init__(self):
        self.generate_keys()
        self.block_size = 214

    def generate_keys(self):
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.public_key()

    def encrypt(self, data):
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_data = b''

        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            encrypted_data += cipher_rsa.encrypt(block)

        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        decrypted_data = b''
        encrypted_block_size = self.private_key.size_in_bytes()

        for i in range(0, len(encrypted_data), encrypted_block_size):
            block = encrypted_data[i:i + encrypted_block_size]
            decrypted_data += cipher_rsa.decrypt(block)

        return decrypted_data
