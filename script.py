#!/usr/bin/python

import os
import confs
import zipfile
import hideFolder
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime

CHAT_CONST = 2000000000

class Driven_Main(object):

	__slots__ = ('config')

	def __init__(self):
		self.config = confs.Config()

	def upload_file(self, path):
		up = VkUpload(self.config.api)
		filename = os.path.basename(path)
		new_uploaded_file = up.document(doc = path,title=filename)
		return new_uploaded_file['doc']['owner_id'], new_uploaded_file['doc']['id']

	def load_file_to_conv(self, owner_id, file_id, chat_id):
		if chat_id < CHAT_CONST:
			chat_id += CHAT_CONST
		msg = f'Container: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}'
		self.config.api.messages.send(peer_id = chat_id, message = msg, attachment = f'doc{owner_id}_{file_id}', random_id = 0)

	def get_all_versions(self, chat_id):
		if chat_id < CHAT_CONST:
			chat_id += CHAT_CONST
		vers = []
		attacs = self.config.api.messages.getHistoryAttachments(peer_id = chat_id, media_type = 'doc', count = 200)
		for att in attacs['items']:
			message = self.config.api.messages.getById(message_ids = att['message_id'])
			file_url = message['items'][0]["attachments"][0]['doc']["url"]
			version = message['items'][0]['text'].split('Container: ')[-1]
			#datetime.strptime('2021-03-01 01:32:23', '%Y-%m-%d %H:%M:%S')
			vers.append([version, file_url])
		return vers





d = Driven_Main()

def start():
	d.config.unlock_file('123')
	d.config.get_api(d.config.data['token']) # todo: if not token; use self.token
	
	#zipf = zipfile.ZipFile('tosend.doc', 'w', zipfile.ZIP_DEFLATED)
	#hideFolder.zipdir('secret', zipf)
	#zipf.close()

	#own, fid = d.upload_file('tosend.doc')
	#d.load_file_to_conv(own, fid, 14)

	#os.remove('tosend.doc')
	print(d.get_all_versions(14))

if not d.config.data:
	token = input('New token: ')
	d.config.get_api(token)
	if type(d.config.api) == vk_api.exceptions.ApiError:
		print('Wrong api key!')
		print(d.config.api)
	else:
		passw = input('New cfg passw: ')
		d.config.new_cfg(token, passw)
		d.config.save()
else:
	start()


