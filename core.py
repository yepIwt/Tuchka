#!/usr/bin/python

"""
	Tuchka - open source cloud on VKontakte servers.
	yepIwt (Sergivesky Nikita), 2023
"""


import confs
import vk_api, requests
import os, zipfile, string, random, shutil
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
		
		logger.debug(f"Запуск функции _search_chat с аргументами title={title}.")

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

		logger.success(f"Успешно найдены чаты с названием `{title}`({len(chats)}).")

		return chats

	def _get_firstlast_name(self, user_id: int) -> tuple:
		
		logger.debug(f"Запуск функции _get_firstlast_name с аргументами user_id={user_id}.")
		
		vk_answer = self.__vk_api.users.get(user_ids = user_id)[0]

		f, l = vk_answer['first_name'], vk_answer['last_name']

		logger.success(f"Успешно получены данные о пользователе {user_id}: {f} {l}.")

		return (f, l)

	
	def add_order_to_files(self, files, order):

		finished_order = [] # Значит, что объект из очереди выгрузился в вк

		for ordered in order:
			for attachments in files:
				if attachments[1] == ordered[1]:
					finished_order.append(ordered)

		new_order = list(set(order) - set(finished_order))

		if new_order:
			files = new_order + files
		return files, new_order

	def _get_history_attachments(self, peer_id: str) -> list:
		
		"""
			Возвращает list подобного типа: [
				(
					from_id, unix_date, url_to_file, commit_message
				),
				...,
				...
			]
		"""

		files = []

		logger.debug(f"Запуск функции _get_history_attachments с аргументами peer_id={peer_id}.")
		
		answer = self.__vk_api.messages.getHistoryAttachments(
			peer_id = peer_id,
			media_type = "doc",
			count = 200
		)

		while vk_answer['items']:

			for file in vk_answer['items']:

				message_id = file['message_id']

				vk_answ = self.__vk_api.messages.getById(
					message_ids = message_id
				)

				files.append(
					(
						file['from_id'],
						file['attachment']['doc']['date'],
						file['attachment']['doc']['url'],
						vk_answ['items'][0]['text']
					)
				)

			vk_answer = self.__vk_api.messages.getHistoryAttachments(
				peer_id = peer_id,
				media_type = "doc",
				count = 200,
				start_from = answer['next_from']
			)

		new_files, new_order = self.add_order_to_files(files, self.cfg.data['order'])

		self.cfg.data['order'] = new_order
		self.cfg.save()

		return new_files

	def __upload_file(self, file_path: str, peer_id: int) -> dict:
		
		"""
			Загрузка файла в ВК в чат
		"""

		if os.access(file_path, os.R_OK):
			
			# Создаем имя файла

			letters = string.ascii_lowercase + string.ascii_lowercase.capitalize()
			file_title = ''.join(random.choice(letters) for i in range(10))

			# Загружаем в ВК

			f = open(file_path, 'rb')
			up = vk_api.VkUpload(self.__vk_api)

			file_data = up.document_message(
				title = file_title,
				doc = f,
				peer_id = peer_id
			)

			return file_data

		return {}

	def __send_file_to_chat(self, file_data: dict, commit_message: str, chat_id: int):
		
		owner_id = file_data['doc']['owner_id']
		file_id = file_data['doc']['id']

		self.__vk_api.messages.send(
			peer_id = chat_id,
			message = commit_message,
			attachment = f"doc{owner_id}_{file_id}",
			random_id = vk_api.utils.get_random_id(),
		)
	
	def change_release(self, url_to_file: str, folder: str):

		# Скачиваем файл
		r = requests.get(url_to_file)
		with open("encrypted", 'wb') as f:
			f.write(r.content)

		# Расшифровываем
		self.cfg.decrypt("encrypted")
		if not os.access(folder, os.R_OK):
			os.mkdir(folder)
		
		# Удаляем старый релиз
		shutil.rmtree(folder)

		# Распаковываем релиз
		unzip_dir("decrypted.zip", folder)

		# Чистим кэш
		os.remove("decrypted.zip")
		os.remove("encrypted")

	def synchronization(self, chat_id: int, commit_message: str):

		"""
			Главный метод в Core. Создает релиз, шифрует и отправляет в вк
		"""

		# Ищем чат архива

		for i in range(len(self.cfg.data['archives'])):
			if self.cfg.data['archives'][i]['id'] == chat_id:
				n = i
				break

		folder = self.cfg.data['archives'][n]['folder']

		if not os.access(folder, os.R_OK):
			os.mkdir(folder)

		# Архивируем данные и шифруем их

		path_to_archive = zip_dir(folder)
		self.cfg.encrypt(path_to_archive)

		# Отправляем в вк

		file_data = self.__upload_file("encrypted", chat_id)
		self.__send_file_to_chat(file_data, commit_message, chat_id)

		# Очищаем кэш
		os.remove("decrypted.zip")
		os.remove("encrypted")

		# Обновляем конфиги
		self.cfg.data['archives'][n]['current'] = file_data['doc']['date']
		self.cfg.save()

		files = self._get_history_attachments(peer_id = chat_id)

		answ = (
			files,
			file_data['doc']['date'],
			file_data['doc']['owner_id'],
			(file_data['doc']['url'],0),
			commit_message
		)

		return answ


if __name__ == "__main__":
	cfg = confs.Config()
	token = os.getenv("VK_TOKEN")
	cfg.new_cfg(token, "12345")
	t = TuchkaCore(cfg)
	tt = t._get_firstlast_name(153798115)
	print(tt)
