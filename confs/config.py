import os
from .cmeth import CryptoMethod
from loguru import logger

logger.add("cash/program_log.log")

class Config:
	
	data = None
	__config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
	__config_here = os.path.isfile(__config_path)

	def __init__(self):
		logger.debug("Initialization Config object")
		logger.debug(f"Config here:{self.__config_here}")

	def open(self, password: str) -> bool:
		logger.debug("Initialization CryptoMethod object")
		self.__cryptomethod = CryptoMethod(password, self.__config_path)
		dec_data = self.__cryptomethod.dec_cfg()
		if dec_data == 0:
			self.data = {}
			logger.debug("Wrong password for config")
			return False
		else:
			self.data = dec_data
			logger.success("Read data from config")
			return True

	def save(self):
		logger.debug("Trying to save config")
		self.__cryptomethod.enc_cfg(self.data)
		logger.success("Config saved")

	def new_cfg(self, vk_api_token: str):
		logger.debug("Trying to create new config")
		data = {
			"vk_api_token": vk_api_token,
			"archive_ids": [],
		}
		self.data = data
		self.__cryptomethod(self.data)
		logger.success("New config saved")