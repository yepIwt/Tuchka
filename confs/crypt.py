from Crypto.Cipher import AES
import hashlib

class LetItCrypt(object):

	__slots__ = ('key','mode','IV')

	def __init__(self,passw):
		self.key = hashlib.sha256(passw.encode('utf-8')).digest()
		self.mode = AES.MODE_CBC
		self.IV = 'This is an IV456'

	def pad_message(self,message):
		while len(message) % 16 != 0:
			message = message + b' '
		return message

	def enc(self,data):
		cipher = AES.new(self.key, self.mode, self.IV)
		padded_message = self.pad_message(data.encode())
		encrypted = cipher.encrypt(padded_message)
		with open('data','wb') as f:
			f.write(encrypted)

	def dec(self):
		cipher = AES.new(self.key, self.mode, self.IV)
		with open('data','rb') as f:
			data = f.read()
		return cipher.decrypt(data).rstrip().decode()

#a = LetItCrypt('123')
#a.enc('hey you. open your eyes')
#print(a.dec())