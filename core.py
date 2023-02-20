#!/usr/bin/python

"""
	Tuchka - open source cloud on VKontakte servers.
	yepIwt (Sergivesky Nikita), 2023
"""


import confs
import vk_api
import os, zipfile
from loguru import logger


VK_MESSAGE_CONSTANT = 2000000000


def get_vk_api(
	login: str = None,
	password: str = None,
	token: str = None,
	) -> tuple:

	logger.debug("Запуск функции get_vk_api.")

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
	
	__cfg = None
	__vk_api = None

	def __init__(self, config_object: confs.Config) -> None:
		
		if type(config_object) != confs.Config:
			logger.critical(f"Неверный тип аргумента config_object. Объект: {config_object}.")

		self.cfg = config_object
		
		token = self.cfg.data.get('vk_api_token')

		if not token:
			logger.critical("В конфиге нет VKAPI токена.")
			exit()
		
		status_code, api = get_vk_api(token = token)

		if not status_code:
			exit()
		else:
			self.__vk_api = api
		
		logger.success("Инициализация класса TuchkaCore произошла успешна.")


	def _create_new_chat(self, title: str) -> int:

		logger.debug(f"Запуск функции _create_new_chat с аргументами title={title}.")
		
		chat_id = self.__vk_api.messages.createChat(title = title)

		logger.success(f"Чат с названием {title} успешно создан с chat_id={chat_id}.")

		return chat_id
	
	def _get_chat_picture(self, peer_id: int) -> str:

		logger.debug(f"Запуск функции _get_chat_picture с аргументами peer_id={peer_id}.")

		vk_answer = self.__vk_api.messages.getChat(
			chat_id = peer_id - VK_MESSAGE_CONSTANT,
		)
		
		url_to_picture = vk_answer.get("photo_200")

		logger.success(f"Успешна полученна ссылка на фото чата {peer_id}: {url_to_picture}.")

		return url_to_picture


	def _get_chat_title(self, peer_id: int) -> str:

		logger.debug(f"Запуск функции _get_chat_title с аргументами peer_id={peer_id}.")

		vk_answer = self.__vk_api.messages.getChat(
			chat_id = peer_id - VK_MESSAGE_CONSTANT,
		)

		chat_title = vk_answer['title']

		logger.success(f"Успешно получено название чата `{chat_title}` для peer_id={peer_id}.")

		return chat_title


	def _get_all_chats(self, with_pictures = False) -> list:

		"""
			Возвращает list подобного типа: [
				(
					peer_id, chat_title, url_to_chat_pic
				),
				...,
				...
				]
		"""

		logger.debug(f"Запуск функции _get_all_chats с аргументами with_pictures={with_pictures}.")

		chats = []

		vk_answer = self.__vk_api.messages.getConversations(
			count = 200, 
			extended = 1
		)

		offset = 0
		while vk_answer['items']:

			for chat_info in vk_answer['items']:

				if chat_info['conversation']['peer']['type'] not in ['user', 'group']:

					chat_pic = None

					if with_pictures:
						chat_pic = self._get_chat_picture(
							chat_info['conversation']['peer']['id']
						)

					chats.append(
						(
							chat_info['conversation']['peer']['id'],
							chat_info['conversation']['chat_settings']['title'],
							chat_pic
						)
					)

			offset += len(vk_answer['items'])

			vk_answer = self.__vk_api.messages.getConversations(
				count = 200,
				extended = 1,
				offset = offset
			)

		logger.success(f"Успешно получена информация о всех чатах ({len(chats)}).")

		return chats


	def _search_chat(self, title: str) -> list:

		"""
			Возвращает list подобного типа: [
				(
					peer_id, chat_title, url_to_chat_pic
				),
				...,
				...
				]
		"""
		
		logger.debug(f"Запуск функции _search_chat с аргументами title={title}")

		chats = []

		vk_answer = self.__vk_api.messages.search(
			q = title,
			count = 100,
		)

		offset = 0
		while vk_answer['items']:

			for chat_info in vk_answer['items']:

				if chat_info['peer_id'] > VK_MESSAGE_CONSTANT:  # Это чат

					flag = False

					for pid, _, _ in chats:

						if pid == chat_info['peer_id']:
							flag = True

					if not flag:

						chats.append(
							(
								chat_info['peer_id'],
								self._get_chat_title(chat_info['peer_id']),
								self._get_chat_picture(chat_info['peer_id'])
							)
						)

			offset += len(vk_answer['items'])

			vk_answer = self.__vk_api.messages.search(
				q = title,
				count = 100,
				offset = offset
			)

		logger.success(f"Успешно найдены чаты с названием `{title}`({len(chats)})")
		return chats

	def _get_firstlast_name(self, uid) -> tuple:
		pass

	def _get_history_attachments(self, peer_id: str) -> list:
		pass


if __name__ == "__main__":
	cfg = confs.Config()
	token = os.getenv("VK_TOKEN")
	cfg.new_cfg(token, "12345")
	t = TuchkaCore(cfg)
	tt = t._search_chat("Хак")
	print(tt)
