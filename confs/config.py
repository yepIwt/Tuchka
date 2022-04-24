import os
from sys import path_hooks
from .cmeth import CryptoMethod
from loguru import logger

import ast

logger.add("cash/program_log.log")


class Config:
	
	data = None
	__config_path = os.path.join(os.getcwd(), "data")
	config_here = os.path.isfile(__config_path)

	def __init__(self):
		logger.debug("Initialization Config object")
		logger.debug(f"Config here:{self.config_here}")

	def open(self, password: str) -> bool:
		logger.debug("Initialization CryptoMethod object")
		self.__cryptomethod = CryptoMethod(password, self.__config_path)
		dec_data = self.__cryptomethod.dec_cfg()
		if dec_data == 0:
			self.data = {}
			logger.debug("Wrong password for config")
			return False
		else:
			self.data = ast.literal_eval(dec_data.decode())
			logger.success("Read data from config")
			return True
	
	def encrypt(self, path_to_file):
		self.__cryptomethod.encrypt_file(path_to_file, "encrypted")
		return os.path.join(path_to_file, "encrypted")
	
	def decrypt(self, path_to_file):
		self.__cryptomethod.decrypt_file(path_to_file, "decrypted.zip")
		return os.path.join(path_to_file, "decrypted.zip")

	def save(self):
		logger.debug("Trying to save config")
		self.__cryptomethod.enc_cfg(str(self.data))
		logger.success("Config saved")

	def new_cfg(self, vk_api_token: str, new_password: str):
		logger.debug("Trying to create new config")
		data = {
			"vk_api_token": vk_api_token,
			"archives": [],
			'order': [],
		}
		self.data = data
		self.__cryptomethod = CryptoMethod(new_password, self.__config_path)
		self.save()
		logger.success("New config saved")