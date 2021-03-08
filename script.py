#!/usr/bin/python

import os
import confs
import zipfile
import hideFolder
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime
import requests as r
CHAT_CONST = 2000000000

class Driven_Main(object):

	__slots__ = ('config','versions')

	def __init__(self):
		self.config = confs.Config()
		self.versions = []

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
		attacs = self.config.api.messages.getHistoryAttachments(peer_id = chat_id, media_type = 'doc', count = 200)
		for att in attacs['items']:
			message = self.config.api.messages.getById(message_ids = att['message_id'])
			file_url = message['items'][0]["attachments"][0]['doc']["url"]
			version = message['items'][0]['text'].split('Container: ')[-1]
			#datetime.strptime('2021-03-01 01:32:23', '%Y-%m-%d %H:%M:%S')
			self.versions.append([version, file_url])
		return self.versions

	def sync(self):
		
		#step1: archive secret to decrypted.zip
		zipf = zipfile.ZipFile('decrypted.zip', 'w', zipfile.ZIP_DEFLATED)
		hideFolder.zipdir('secret', zipf)
		zipf.close()

		#step2: encrypt decrypted.zip to container
		self.config.crypter.enc_file()

		#step3: send container
		ow, fi = self.upload_file('container')
		self.load_file_to_conv(ow,fi, 14)
		
		#step4: delete old file
		os.remove('decrypted.zip')
		
		#step5: mount new container
		print('Mounted')

	def change_version(self, n: int):
		#vers = self.get_all_versions(chat_id)
		link = self.versions[n][-1]

		#step1: download new container
		file_in_url = r.get(link)
		with open('containerNEW','wb') as f:
			f.write(file_in_url.content)

		#step2: umount container
		os.system('./mount_sudo.sh 0 /home/yepiwt/test')
		print('Umounted')

		#step3: delete secret and container
		os.remove('container')
		#step3.1: rename containers
		os.rename('containerNEW','container')
		os.rmdir('/home/yepiwt/Driven/secret')

		#step4: unlock container
		self.config.dec_file()

		#step5: unzip decrypted.zip 
		hideFolder.unzipdir('decrypted.zip')

		#step6: mount new container
		os.system('./mount_sudo.sh 1 secret /home/yepiwt/test')







d = Driven_Main()

def start():
	d.config.unlock_file('123')
	d.config.get_api(d.config.data['token']) # todo: if not token; use self.token
	#d.sync()
	versions = d.get_all_versions(14)
	n = 1
	#for n, container_info in enumerate(versions):
		#container_info[0] - date; container_info[1] - link
	#	print(n,container_info[0])
	d.change_version(n)

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


