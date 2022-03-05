#!/usr/bin/python

"""
	Driven (Tuchka) program core
	yepIwt, 2022
"""

import vk_api
import confs

from loguru import logger

VK_MESSAGE_CONSTANT = 2000000000

def get_vk_api(login: str = None, password: str = None, token: str = None):
	
	vk_session = vk_api.VkApi(
		login = login,
		password = password,
		token = token
	)

	api = vk_session.get_api()

	try:
		api.wall.get()
	except Exception as err:
		return False, err
	else:
		return True, api

class DrivenCore:

	cfg = None
	_vk_api = None

	def __init__(self, config: confs.Config):
		"""
			Recomendation: use only working vk api token or add a handler before
		"""
		self.cfg = config
		status, self._vk_api = get_vk_api(token = self.cfg.data['vk_api_token'])
		logger.success('VK API granted!')

	def _get_all_chats(self) -> list:
		
		chats = []
		
		logger.debug("Started getting all chats")
		answer = self._vk_api.messages.getConversations(count = 200, extended = 1)
		offset = 0

		while answer['items']:
			for i in answer['items']:
				if i['conversation']['peer']['type'] not in ['user', 'group']:
					chats.append(
						(
							i['conversation']['peer']['id'], 
							i['conversation']['chat_settings']['title']
						)
					)
			offset += len(answer['items'])
			answer = self._vk_api.messages.getConversations(count = 200, extended = 1, offset = offset)

		logger.success("Got all chats from acc ->", len(chats))
		return chats

	def _search_chat_by_title(self, text: str):

		chats = []
		
		logger.debug(f"Started searching in all chats with key = {text}")
		answer = self._vk_api.messages.search(
			q = text,
			count = 100,
		)

		offset = 0
		while answer['items']:
			for i in answer['items']:

				if i['peer_id'] > VK_MESSAGE_CONSTANT: # This is a chat

					answer2 = self._vk_api.messages.getChat(chat_id = i['peer_id'] - VK_MESSAGE_CONSTANT)
					flag = False

					for pid,title in chats:
						if pid == i['peer_id']:
							flag = True

					if not flag:
						chats.append(
							(
								i['peer_id'],
								answer2['title']
							)
						)

			offset += len(answer['items'])
			answer = self._vk_api.messages.search(q = text, count = 100, offset = offset)
		return chats

	def _get_chat_picture(self):
		pass
	
	def _get_attachments_history(self):
		pass

	def _upload_file(self):
		pass

	def _change_release(self):
		pass

if __name__ == "__main__":
	c = confs.Config()
	if c._config_here:
		unlocked = False
		while unlocked != True:
			password = input("Enter password: ")
			unlocked = c.open(password)
		print("Done!")
	else:
		status = False
		while status != True:
			api_token = input("Enter VK API token: ")
			status, err = get_vk_api(token = api_token)
			if not status:
				print(err)
		new_password = input("Enter new password: ")
		c.new_cfg(api_token, new_password)
		print("Done!")