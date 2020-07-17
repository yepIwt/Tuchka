#	Rewrite!
#	https://github.com/serg1evsky
#	2020

import os
import modules
import requests
from vk_api import VkApi
from vk_api import VkUpload
from vk_api import exceptions
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

				for section in self.sections:
					self.find_folders(section)
					for folder in section['folders']:
						self.find_files(section,folder)
			else:
				print('No Cfg\'s')
				self.new_section(input('Wi will create new section. Tell me title'))
		return self.sections

	def try_outdate(section,folder):
		pass

	def outdated_folder(self,folder):
		fi = 0
		si = 0
		for i in range(len(self.sections)):
			for k in range(len(self.sections[i]['folders'])):
				if self.sections[i]['folders'][k]['title_fd'] == folder['title_fd']:
					fi = k
					break
			si = i
			break
		files = ''
		del1 = []
		for j in range(len(self.sections[si]['folders'][fi]['files'])):
			self.download_file(self.sections[si]['folders'][fi]['files'][j]['name'],self.sections[si]['folders'][fi]['files'][j]['down_link'])
			obj = self.upload_file(self.sections[si]['folders'][fi]['files'][j]['name'])
			self.sections[si]['folders'][fi]['files'][j]['down_link'] = obj['doc']['url']
			files += 'doc' + str(self.masterid) + '_' + str(obj['doc']['id']) + ','
			del1.append(obj['doc']['id'])
			os.remove(self.sections[si]['folders'][fi]['files'][j]['name'])
		self.delete_folder(folder)
		new_id = self.new_folder(self.sections[si]['title'],folder['title_fd'])
		self.sections[si]['folders'][fi]['fd_id'] = int(new_id)
		self.client.messages.edit(
			peer_id = 2000000000+int(self.sections[si]['id']),
			message_id = self.sections[si]['folders'][fi]['fd_id'],
			message = '&#128193;' + self.sections[si]['folders'][fi]['title_fd'],
			attachment = files,
		)
		self.sections[si]['folders'].pop(fi)
		for trash in del1:
			self.client.docs.delete(
				owner_id=int(self.masterid),
				doc_id=int(trash),
			)
		return self.sections

	def create_section(self,id_sec=None,title=None):
		obj = {
			'id':id_sec,
			'title':title,
			'folders':[]
		}
		return obj

	def create_folder(self,fd_id=None,title_fd=None,files=[]):
		obj = {
			'fd_id':fd_id,
			'title_fd':title_fd,
			'files':files
		}
		return obj

	def create_file(self,name_f=None,type_f=None,down_link=None):
		obj = {
			'name':name_f,
			'type':type_f,
			'down_link':down_link,
		}
		return obj

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

	def edit_section(self,section,folder=None,fd_n=None,file=None):
		if folder:
			section['folders'].append(folder)
		else:
			section['folders'][fd_n]['files'].append(file)
		return self.sections

	def new_folder(self,section_name,title):
		section = self.get_section_by_name(section_name)
		obj = self.client.messages.send(
			chat_id = int(section['id']),
			message = '&#128193;' + str(title),
			random_id=get_random_id(),
			)
		self.edit_section(section,folder=self.create_folder(obj,title))
		return obj

	def delete_folder(self,folder):
		self.client.messages.delete(
				message_id=folder['fd_id']
			)

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

	def find_files(self,section,folder):
		obj = self.client.messages.getById(
				message_ids=folder['fd_id'],
			)
		for i in range(len(section['folders'])):
			if section['folders'][i]['fd_id'] == folder['fd_id']:
				fd_n = i
				break
		for file in obj['items'][0]['attachments']:
			self.edit_section(section,fd_n=i,file=self.create_file(name_f=file['doc']['title'],type_f=file['doc']['type'],down_link=file['doc']['url']))
		return self.sections

	def upload_file(self,doc,title=None):
		a = VkUpload(self.client)
		if not title:
			title = os.path.basename(doc)
		return a.document(doc,title)

	def delete_file(self,doc_id):
		obj = self.client.docs.delete(
			owner_id = self.masterid,
			doc_id=doc_id
			)
		return obj

	def download_file(self,name,link):
		f = open(name,'wb')
		file = requests.get(link)
		f.write(file.content)
		f.close()

	def add_file_to_folder(self,section_name,title_fd,file,filename=None):
		folder = 0
		section = self.get_section_by_name(section_name)
		for i in range(len(section['folders'])):
			if section['folders'][i]['title_fd'] == title_fd:
				ifolder = i
				folder = section['folders'][i]
				break
		obj = self.upload_file(  ile,filename)
		self.edit_section(section,fd_n=ifolder,file=self.create_file(name_f=obj['doc']['title'],type_f=obj['doc']['type'],down_link=obj['doc']['url']))
		nowfiles = ""
		for file in section['folders'][i]['files']:
			nowfiles += 'doc'+ str(self.masterid) + '_' + str(file['id_f']) + ','
		try:
			self.client.messages.edit(
				peer_id=2000000000+int(section['id']),
				message_id=section['folders'][ifolder]['fd_id'],
				message='&#128193;'+str(section['folders'][ifolder]['title_fd']),
				attachment=nowfiles,
				keep_forward_messages=1,
				dont_parse_links=1,
				keep_snippets=1,
			)
		except exceptions.ApiError:
			print('This message is too old')
			self.outdated_folder(section,folder)
		self.delete_file(obj['doc']['id'])
		return self.sections

#cloud = RatherCloudy(token)
#cloud.cfg()
#cloud.cfg('save')
