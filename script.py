#!/usr/bin/python

import os, platform
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
		print('Downloaded new container')

		#step2: umount container
		try:
			os.rmdir(self.config.data['localdir'])
		except:
			pass # TODO: trace this moment
		print('Local folder cleared')

		#step3: delete secret and container
		os.remove(os.path.join(os.path.dirname(__file__), 'container'))
		#step3.1: rename containers
		os.rename('containerNEW','container')
		
		#step4: unlock container
		self.config.crypter.dec_file()

		#step5: unzip decrypted.zip 
		hideFolder.unzipdir('decrypted.zip',os.path.join( os.path.dirname(self.config.data['localdir']),''))
		
		#step6: delete decrypted.zip
		os.remove(os.path.join(os.path.dirname(__file__),'decrypted.zip'))
		
		

def start():
	d.config.unlock_file('123')
	d.config.get_api(d.config.data['token']) # todo: if not token; use self.token
	#d.sync()
	d.get_all_versions(14)
	n = 3
	#for n, container_info in enumerate(versions):
		#container_info[0] - date; container_info[1] - link
	#	print(n,container_info[0])
	d.change_version(n)

if __name__ == '__main__':
	d = Driven_Main()
	if not d.config.data:
		token = input('New token: ')
		d.config.get_api(token)
		if type(d.config.api) == vk_api.exceptions.ApiError:
			print(f'Wrong api key: {d.config.api}')
		else:
			passw = input('New cfg passw: ')
			patch = '~'
			folder_location = input(f'Enter path to local folder. Default folder - {os.path.join(os.path.expanduser(patch), confs.FOLDER_NAME)}: ')
			if not folder_location:
				folder_location = os.path.join(os.path.expanduser('~'), confs.FOLDER_NAME)
			try:
				os.mkdir(folder_location)
			except FileExistsError:
				pass
			except FileNotFoundError:
				print('Incorrect path. Using default folder')
				folder_location = os.path.join(os.path.expanduser('~'), confs.FOLDER_NAME)
			d.config.new_cfg(token, passw, folder_location)
			d.config.save()
			start()
	else:
		start()



