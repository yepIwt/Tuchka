#	Rewrite!
#	https://github.com/serg1evsky
#	2020

import os
import modules
from vk_api import VkApi
from vk_api import VkUpload
from vk_api.utils import get_random_id


class RatherCloudy(object):

	__slots__ = ('client', 'masterid','sections')

	def __init__(self,token):
		session = VkApi(token = token, api_version=5.103)
		self.client = session.get_api()
		self.sections = []
		self.masterid = self.client.users.get()[0]['id']

	def cfg(self,move=None):
		if move: # сохранить
			with open('config.cfg','w') as f:
				f.write('Sections:')
				for section in self.sections:
					f.write('\n' + str(section['id']) + ':' + str(section['title']))
				f.close()
		else: # считать
			if os.path.isfile('config.cfg'):
				f = open('config.cfg')
				l = [line.strip('\n') for line in f]
				l.remove(l[0]) 
				for i in range(len(l)):
					self.sections.append(self.create_section(id_sec=l[i][:l[i].index(':')],title=l[i][l[i].index(':')+1:]))
			else:
				print('No Cfg\'s')
				self.new_section(input('Wi will create new section. Tell me title'))
		for section in self.sections:
			self.find_folders(section)
		return self.sections			

	def create_section(self,id_sec=None,title=None):
		obj = {
			'id':id_sec,
			'title':title,
			'folders':[]
		}
		return obj

	def create_folder(self,fd_id=None,title_fd=None):
		obj = {
			'fd_id':fd_id,
			'title_fd':title_fd,
			'files':[]
		}
		return obj

	def create_file(self,name_f=None,type_f=None,id_f=None):
		obj = {
			'name':name_f,
			'type':type_f,
			'id_f':id_f
		}
		return obj
		
	def edit_section(self,section,folder=None,fd_n=None,file=None):
		if folder:
			section['folders'].append(folder)
		if fd_n:
			section['folders'].append(file)
		return self.sections

	def new_section(self,title):
		id = self.client.messages.createChat(
			user_ids=self.masterid,
			title=title,
			)
		self.sections.append(self.create_section(id_sec=id,title=title))
		return self.sections
	
	def get_section_by_name(self,section_name):
		for section in self.sections:
			if section['title'] == section_name:
				gotcha = section
				break
		if not gotcha:
			print('Не могу найти раздел')
			return False
		return gotcha

	def new_folder(self,section_name,title):
		section = self.get_section_by_name(section_name)
		obj = self.client.messages.send(
			chat_id = int(nowsection['id']),
			message = '&#128193;' + str(title),
			random_id=get_random_id(),
			)
		return obj

	def edit_folder_name(self,section_name,past_name,title):
		section = self.get_section_by_name(section_name)
		for folder in section['folders']:
			if folder['title_fd'] == past_name:
				previos = folder
		self.client.messages.edit(
				peer_id=2000000000+int(section['id']),
				message='&#128193;' + str(title),
				message_id=folder['fd_id'],
			)
		return self.sections

	def find_folders(self,section):
		obj = self.client.messages.search(
				q='&#128193;',
				peer_id=2000000000+int(section['id']),
				count=100,
			)
		for item in obj['items']:
			self.edit_section(section,folder=self.create_folder(item['id'],item['text'][1:]))
		return self.sections
	


cloud = RatherCloudy('token')
cloud.cfg()
cloud.cfg('save')
