#!/usr/bin/python

"""
	Driven (Tuchka) program core
	yepIwt, 2022
"""

import os
import vk_api
import confs

from loguru import logger

VK_MESSAGE_CONSTANT = 2000000000


def get_vk_api(login: str = None, passw: str = None, token: str = None) -> tuple:

	vk_session = vk_api.VkApi(
		login = login,
		password = passw,
		token = token
	)

	api = vk_session.get_api()

	try:
		api.wall.get()
	except Exception as error:
		return False, error
	else:
		return True, api


class DrivenCore:

	cfg = None
	_vk_api = None
	_current_chat_selected = None # peer_id

	def __init__(self, config: confs.Config):

		"""
			Recommendation: use only working vk api token or add a handler before
		"""

		self.cfg = config
		_, self._vk_api = get_vk_api(token=self.cfg.data['vk_api_token'])
		logger.success('VK API granted!')

	def _get_all_chats(self) -> list:

		"""
			Returns list with: peer_id, chat_title, url_to_chat_pic
		"""

		chats = []

		logger.debug("Start 'get_all_chats' function")
		answer = self._vk_api.messages.getConversations(count=200, extended=1)
		offset = 0

		while answer['items']:
			for i in answer['items']:
				if i['conversation']['peer']['type'] not in ['user', 'group']:
					chats.append(
						(
							i['conversation']['peer']['id'],
							i['conversation']['chat_settings']['title'],
							self._get_chat_picture_url_by_peer_id(i['conversation']['peer']['id'])
						)
					)
			offset += len(answer['items'])
			answer = self._vk_api.messages.getConversations(count=200, extended=1, offset=offset)

		logger.success(f"End 'get_all_chats' function with len(result) = {len(chats)}")
		return chats

	def _get_chat_title_by_peer_id(self, peer_id: int) -> str:
		logger.debug(f"Start 'get_chat_title_by_peer_id' function with peer_id = {peer_id}")

		answer = self._vk_api.messages.getChat(
			chat_id=peer_id - VK_MESSAGE_CONSTANT,
		)
		chat_title = answer['title']

		logger.success("End 'get_all_chats' function")
		return chat_title

	def _get_chat_picture_url_by_peer_id(self, peer_id: int) -> str:
		logger.debug(f"Start 'get_chat_picture_url_by_peer_id' function with peer_id = {peer_id}")

		answer = self._vk_api.messages.getChat(
			chat_id=peer_id - VK_MESSAGE_CONSTANT,
		)
		url_to_picture = answer.get("photo_200")

		logger.success("End 'get_chat_picture_url_by_peer_id' function")
		return url_to_picture

	def _search_chat_by_title(self, text: str) -> list:

		"""
			Returns list with: peer_id, chat_title, url_to_chat_pic
		"""

		chats = []

		logger.debug(f"Start 'search_chat_by_title' function with q = {text}")

		answer = self._vk_api.messages.search(
			q=text,
			count=100,
		)

		offset = 0
		while answer['items']:
			for i in answer['items']:

				if i['peer_id'] > VK_MESSAGE_CONSTANT:  # This is a chat

					flag = False

					for pid, _, _ in chats:
						if pid == i['peer_id']:
							flag = True

					if not flag:
						chats.append(
							(
								i['peer_id'],
								self._get_chat_title_by_peer_id(i['peer_id']),
								self._get_chat_picture_url_by_peer_id(i['peer_id'])
							)
						)

			offset += len(answer['items'])
			answer = self._vk_api.messages.search(q=text, count=100, offset=offset)

		logger.success(f"End 'search_chat_by_title' function with len(result) = {len(chats)}")
		return chats

	def _get_history_attachments_by_peer_id(self, peer_id: str) -> list:

		"""
			Returns list with tuple: from_id, unix_date, url_to_file, commit_message
			Warning: Duplicate files expected.
		"""

		files = []

		logger.debug(f"Start 'get_history_attachments_by_peer_id' with peer_id = {peer_id}")

		answer = self._vk_api.messages.getHistoryAttachments(
			peer_id=peer_id,
			media_type="doc",
			count=200
		)

		while answer['items']:

			for it in answer['items']:

				message_id = it['message_id']
				answ = self._vk_api.messages.getById(message_ids = message_id)

				from_id = it['from_id']
				date_unix = it['attachment']['doc']['date']
				url_to_file = it['attachment']['doc']['url']
				commit_message = answ['items'][0]['text']

				files.append(
					(
						from_id,
						date_unix,
						url_to_file,
						commit_message
					)
				)

			answer = self._vk_api.messages.getHistoryAttachments(
				peer_id=peer_id,
				media_type="doc",
				count=200,
				start_from=answer['next_from']
			)

		logger.success(f"End 'get_history_attachments_by_peer_id' function with len(result) = {len(files)}")
		return files

	def _upload_file(self, file_path) -> dict:
		if os.access(file_path, os.R_OK):
			file_title = "there_must_be_random_string"
			f = open(file_path, 'rb')
			up = vk_api.VkUpload(self._vk_api)
			file_data = up.document(
				title = file_title,
				doc = f
			)
			return file_data
		return {}
	
	def _send_file_to_chat_id(self, file_data, commit_message, chat_id):
		
		owner_id = file_data['doc']['owner_id']
		file_id = file_data['doc']['id']

		self._vk_api.messages.send(
			peer_id = chat_id,
			message = commit_message,
			attachment = f"doc{owner_id}_{file_id}",
			random_id = vk_api.utils.get_random_id(),
		)

	def _change_release(self):
		pass

	def synchronization(self, file_id, commit_message, chat_id):
		file_data = self._upload_file(file_id)
		self._send_file_to_chat_id(file_data, commit_message, chat_id)

if __name__ == "__main__":
	c = confs.Config()
	if c.config_here:
		unlocked = False
		while not unlocked:
			password = input("Enter password: ")
			unlocked = c.open(password)
		print("Done!")
	else:
		status = False
		api_token = ""
		while not status:
			api_token = input("Enter VK API token: ")
			status, err = get_vk_api(token=api_token)
			if not status:
				print(err)
		new_password = input("Enter new password: ")
		c.new_cfg(api_token, new_password)
		print("Done!")
