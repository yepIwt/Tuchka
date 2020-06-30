import os
from vk_api import VkApi
from vk_api import VkUpload
from vk_api.utils import get_random_id 

class RatherCloudy(object):

	__slots__ = ('session','vk','linkmaster','folders', 'client','files')

	def __init__(self, token):
		self.session = VkApi(token=token, api_version=5.103)
		self.client = self.session.get_api()
		self.folders = []
		self.linkmaster = self.client.users.get()[0]['id']

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

	def get_docs(self, count: int, offset: int, type: int):
		"""
     	:param count: Сколько документов вернуть
     	:param offset: Оффсет,че
     	:param type: Тип документа (https://vk.com/dev/docs.get)
     	:param owner_id: Чьи документы вернуть
     	"""
		docs = self.client.docs.get(
     		count=count,
     		offset=offset,
     		type=type,
     		owner_id=self.linkmaster,
     		)
		return docs

	def new_folder(self, title: str):
		"""
		:param title: Название папки
		"""
		id = [self.client.messages.createChat(
			user_ids=self.linkmaster,
			title=title,
			)]
		temp = [str(id)+":"+str(title)]
		self.folders.append(temp)
		self.folders[len(self.folders)-1].append([])
		return self.folders
	#ne rabotaet
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
		self.folders = [['5:Gays',[]]]
		with open('config.cfg','w') as f:
			f.write('Folders:\n')
			for folder in self.folders:
				f.write(self.wee('',folder)+":"+self.wee('name',folder)+ '\n')
			f.close()

	def read_cfg(self):
		if os.path.isfile('config.cfg'):
			f = open('config.cfg')
			for line in f:
				self.folders.append([line[:line.index('\n')]])
				self.folders[len(self.folders)-1].append([])
			self.folders.remove(self.folders[0])
		else:
			print("No cfgs")
			print("We have to create new folder")
			print("Title: ",end= "")
			self.new_folder(input())

		return self.folders

	def wee(self,type,folder):
		if type == 'name':
			return folder[0][folder[0].index(':')+1:]
		else:
			return folder[0][:folder[0].index(':')]

	def check_folders(self):
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
				

	def get_filles_from_folder(self):
		for folder in self.folders:
			print('This is', folder[0], self.client.messages.getHistoryAttachments(peer_id=2000000000+int(self.wee('id',folder)),media_type='doc'))

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
				upload_machine.document(file,title=title)['id']
#cloud = RatherCloudy("")
#print(cloud.read_cfg())
#cloud.get_filles_from_folder()