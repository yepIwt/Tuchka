from Crypto.Cipher import AES
import hashlib

password = b'testtest'
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = 'This is an IV456'

def pad(file):
    while len(file) % 16 != 0:
        file = file + ' '
    return file

def encrypt(message):
    padded_message = pad(message).encode()
    cipher = AES.new(key, mode, IV)
    encrypted_message = cipher.encrypt(padded_message)
    with open('data','wb') as f:
        f.write(encrypted_message)

def decrypt():
    with open('data','rb') as f:
        encrypted_data = f.read()
    cipher = AES.new(key, mode, IV)
    decrypted = cipher.decrypt(encrypted_data).rstrip().decode()
    print(decrypted)

encrypt('sex')
decrypt()
