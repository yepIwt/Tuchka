import os
import modules
from vk_api import VkApi
from vk_api import VkUpload
from vk_api.utils import get_random_id 


class RatherCloudy(modules.withfolder):

	__slots__ = ('session','vk','linkmaster','folders', 'client','files','withfolders')

	def __init__(self, token, dir=None):
		self.session = VkApi(token=token, api_version=5.103)
		self.client = self.session.get_api()
		self.folders = []
		self.linkmaster = self.client.users.get()[0]['id']
		if dir == None:
			super().__init__(os.getcwd())
		else:
			super().__init__(dir)
		
	def send_message(self,message: str,attachment=None, keyboard=None):
		"""
		:param user_id: Кому отправлять(id)
		:param message: message
		:param peer_id: id польщователя у тебя в диалогах(можно использовать id страницы)
		:param attachment: Вложение(документ)
		:param keyboard: Клавиатура(для бота)
		"""

		self.client.messages.send(
            chat_id=7,
            message=message,
            random_id=get_random_id(),
            attachment="doc543325423_556356447",
        )

	def new_folder(self, title):
		"""
		:param title: Название папки
		"""
		id = self.client.messages.createChat(
			user_ids=self.linkmaster,
			title=title,
			)
		self.folders.append([str(id) + ':' + str(title)])
		self.folders[len(self.folders)-1].append([])
		return self.folders

	def del_folder(self,title:str):
		self.client.messages.removeChatUser(
			chat_id=self.folders[folders.index(title)],
			user_id=self.linkmaster,
			)
		self.client.messages.deleteConversation(
			user_id=2000000000+int(self.folders[self.folders.index(title)]),
			peer_id=user_id,
			)
		return True

	def save_cfg(self):
		with open('config.cfg','w') as f:
			f.write('Folders:\n')
			for folder in self.folders:
				this = str(self.wee('id',folder)) + ':' + self.wee('name',folder)
				f.write(this + '\n')
			f.close()

	def read_cfg(self):
		if os.path.isfile('config.cfg'):
			f = open('config.cfg')
			for line in f:
				self.folders.append([line[:line.index('\n')]])
				self.folders[len(self.folders)-1].append([])
			self.folders.remove(self.folders[0]) 
		else:
			print('No cfgs')
			new_folder(str(input('We will create new folder on your cloud. Tell me name')))
		return self.folders
	
	def wee(self,type,folder):
		if type == 'name':
			return folder[0][folder[0].index(':')+1:]
		elif type == 'files':
			return folder[1]
		elif type == 'name2':
			tmp = []
			for obj in folder:
				tmp.append(self.wee('name',obj))
			return tmp
		else:
			return folder[0][:folder[0].index(':')]

	def check_folders_by_name(self):
		for folder in self.folders:
			try:
				cur_cloud = self.client.messages.getChat(chat_id=self.wee('id',folder))['title']
			except:
				print('Invalid folder',folder)
				exit()
			if cur_cloud == self.wee('name',folder):
				print('Synced:', folder[0])
			else:
				self.client.messages.editChat(chat_id=int(self.wee('',folder)),title=self.wee('name',folder))
				print('Title changed:', cur_cloud,'-->',self.wee('name',folder))
				print('Synced:', folder[0])
				

	def get_filles_from_folder(self,folder):
		return self.client.messages.getHistoryAttachments(peer_id=2000000000+int(self.wee('id',folder)),media_type='doc')

	def send(self,file,title:str):
		"""Загрузка файла
		:param file: Сам файл
		"""
		if not os.path.isfile(file):
			print('I can\'t find it')
		else:
			if not self.folders:
				print('You don\'t have any folders')
			else:
				upload_machine = VkUpload(self.client)
				print(upload_machine.document(file,title=title)['id'])
	
	def download_folder(self,title): #disabled
		for folder in self.folders:
			if self.wee('name',folder) == title:
				files = self.get_filles_from_folder(folder)
				print(files)


#cloud = RatherCloudy("token",'dir')
#cloud.read_cfg()
#cloud.check_folders_by_name()
#cloud.check_folders_from_cloud(cloud.folders)
#cloud.save_cfg()