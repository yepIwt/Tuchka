from Crypto.Cipher import AES
import hashlib
import os

class CryptoMethod:

	def __init__(self, passw: str, path_to_config: str):
		self.key = hashlib.sha256(passw.encode()).digest()
		self.mode = AES.MODE_EAX
		self.cfg_path = path_to_config

	def pad(self, text: bytes) -> bytes:
		while len(text) % 16 != 0:
			text += b' '
		return text

	def enc_cfg(self, data: str) -> None:
		cipher = AES.new(self.key, self.mode)
		ciphertext, tag = cipher.encrypt_and_digest(data.encode())
		with open(self.cfg_path, "wb") as file_out:
			[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]

	def dec_cfg(self) -> str:
		file_in = open(self.cfg_path, "rb")
		nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
		cipher = AES.new(self.key, self.mode, nonce)
		try:
			data = cipher.decrypt_and_verify(ciphertext, tag)
		except ValueError:
			return 0 # empty string like False
		else:
			return data

	def encrypt_file(self, start_path: str, end_path: str) -> None:
		"""
			start_path: decrypted.zip
			end_path: encrypted.zip
		"""

		cipher = AES.new(self.key, self.mode)
		with open(start_path,'rb') as f:
			decrypted_data = f.read()
		ciphertext, tag = cipher.encrypt_and_digest(decrypted_data)
		with open(end_path, "wb") as file_out:
			[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]

	def decrypt_file(self, end_path: str, start_path: str) -> bool:
		"""
			end_path: encrypted.zip
			start_path: decrypted.zip
		"""

		file_in = open(end_path, "rb")
		nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
		cipher = AES.new(self.key, self.mode, nonce)
		try:
			data = cipher.decrypt_and_verify(ciphertext, tag)
		except Exception as err:
			raise err
		else:
			with open(start_path,'wb') as f:
				f.write(data)
			return True