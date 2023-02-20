#!/usr/bin/python

"""
	Tuchka - open source cloud on VKontakte servers.
	yepIwt (Sergivesky Nikita), 2023
"""


import os, zipfile
import vk_api
from loguru import logger


def get_vk_api(
	login: str = None,
	password: str = None,
	token: str = None,
	) -> tuple:

	logger.debug("Запуск функции get_vk_api")

	vk_session = vk_api.VkApi(
		login = login,
		password = password,
		token = token
	)

	api = vk_session.get_api()

	try:
		api.messages.getConversations()
	except Exception as err:
		logger.critical(f"Не получен VKAPI. {err}.")
		return False, err
	else:
		logger.success("VKAPI успешно получен.")
		return True, api


def zip_dir(path: str) -> str:

	logger.debug("Запуск функции zip_dir")

	path_to_file = os.path.abspath('decrypted.zip')

	zipf = zipfile.ZipFile(path_to_file, "w", zipfile.ZIP_DEFLATED)

	with zipf as zf:
		for dirname, _, files in os.walk(path):
			for filename in files:
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(os.path.abspath(path)) + 1:]
				zf.write(absname, arcname)
	zf.close()

	logger.success(f"zip_dir сохранил файл по пути: {path_to_file}")

	return path_to_file


def unzip_dir(path_to_archive: str, folder_path: str) -> str:

	logger.debug("Запуск функции unzip_dir")

	try:
		with zipfile.ZipFile(path_to_archive, 'r') as file:
			file.extractall(folder_path)
	except Exception as err:
		logger.critical(f"Не получилось разархивировать архив. {err}.")
		exit()
	else:
		logger.success(f"Файл разархивирован по пути: {folder_path}")
		return folder_path


class TuchkaCore:
	
	def __init__(self) -> None:
		pass

	def _create_new_chat(self, title: str) -> None:
		pass

	def _get_all_chats(self, with_pictures = False) -> list:
		pass
	
	def _get_chat_title(self, peer_id: int) -> str:
		pass

	def _get_chat_picture(self, peer_id: int) -> str:
		pass

	def _search_chat(self, title: str) -> list:
		pass

	def _get_firstlast_name(self, uid) -> tuple:
		pass

	def _get_history_attachments(self, peer_id: str) -> list:
		pass
