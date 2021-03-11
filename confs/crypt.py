from Crypto.Cipher import AES
import hashlib
import os

class LetItCrypt(object):

	def __init__(self, passw: str):
		self.key = hashlib.sha256(passw.encode()).digest()
		self.mode = AES.MODE_CBC
		self.IV = 'This is an IV456'

	def pad(self, text: bytes) -> bytes:
		while len(text) % 16 != 0:
			text = text + b' '
		return text

	def enc_cfg(self, data: str) -> None:
		cipher = AES.new(self.key, self.mode, self.IV)
		padded = self.pad(data.encode())
		encrypted_data = cipher.encrypt(padded)
		with open('data','wb') as f:
			f.write(encrypted_data)

	def dec_cfg(self) -> str:
		cipher = AES.new(self.key, self.mode, self.IV)
		with open('data','rb') as f:
			encrypted_data = f.read()
		try:
			return cipher.decrypt(encrypted_data).rstrip().decode()
		except:
			return ''

	def enc_file(self) -> None:
		cipher = AES.new(self.key, self.mode, self.IV)
		with open('decrypted.zip','rb') as f:
			decrypted_data = f.read()
		padded = self.pad(decrypted_data)
		encrypted_data = cipher.encrypt(padded)
		with open('container','wb') as f:
			f.write(encrypted_data)

	def dec_file(self) -> None:
		cipher = AES.new(self.key, self.mode, self.IV)
		with open('container','rb') as f:
			encrypted_data = f.read()
		decrypted_data = cipher.decrypt(encrypted_data)
		with open('decrypted.zip','wb') as f:
			f.write(decrypted_data)