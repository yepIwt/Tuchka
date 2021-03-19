from Crypto.Cipher import AES
import hashlib
import os

class LetItCrypt(object):

	def __init__(self, passw: str):
		self.key = hashlib.sha256(passw.encode()).digest()
		self.mode = AES.MODE_EAX

	def pad(self, text: bytes) -> bytes:
		while len(text) % 16 != 0:
			text += b' '
		return text

	def enc_cfg(self, data: str) -> None:
		cipher = AES.new(self.key, self.mode)
		ciphertext, tag = cipher.encrypt_and_digest(data.encode())
		file_out = open("data", "wb")
		[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
		file_out.close()

	def dec_cfg(self) -> str:
		file_in = open("data", "rb")
		nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
		cipher = AES.new(self.key, self.mode, nonce)
		try:
			data = cipher.decrypt_and_verify(ciphertext, tag)
		except ValueError:
			return ''
		else:
			return data

	def enc_file(self) -> None:
		cipher = AES.new(self.key, self.mode)
		with open('decrypted.zip','rb') as f:
			decrypted_data = f.read()
		ciphertext, tag = cipher.encrypt_and_digest(decrypted_data)
		file_out = open("container", "wb")
		[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
		file_out.close()

	def dec_file(self) -> None:
		file_in = open("container", "rb")
		nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
		cipher = AES.new(self.key, self.mode, nonce)
		try:
			data = cipher.decrypt_and_verify(ciphertext, tag)
		except:
			print('Something wrong with container')
			exit()
		else:
			with open('decrypted.zip','wb') as f:
				f.write(data)