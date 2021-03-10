#!/usr/bin/python

import os, sys
import confs, hideFolder
import zipfile
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime
import requests as r
#QT
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from ui.locker import Ui_Locker
from ui.mainwindow import Ui_Menu

CHAT_CONST = 2000000000
ERROR_LOCATION = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке: </span><span style=" font-size:20pt; font-weight:600; color:#ff0000;">Ошибка</span></p></body></html>'
SUCCES_LOCAL = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке: </span><span style=" font-size:20pt; font-weight:600; color:#00ff08;">Успех</span></p></body></html>'
ERROR_TOKEN = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи: </span><span style=" font-size:20pt; font-weight:600; color:#ff0000;">Ошибка</span></p></body></html>'
SUCCES_TOKEN = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи: </span><span style=" font-size:20pt; font-weight:600; color:#00ff08;">Успех</span></p></body></html>'

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
		self.config.get_api(self.config.data['token'])
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
		hideFolder.zipdir(self.config.data['localdir'], zipf)
		zipf.close()

		#step2: encrypt decrypted.zip to container
		self.config.crypter.enc_file()

		#step3: send container
		ow, fi = self.upload_file('container')
		self.load_file_to_conv(ow,fi, 14)
		
		#step4: delete old file
		os.remove('decrypted.zip')

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

class Locker(QMainWindow):
	__slots__ = ('d','new_credentials')
	def __init__(self):
		super(Locker, self).__init__()
		self.ui = Ui_Locker()
		self.ui.setupUi(self)
		self.w = None
		self.d = Driven_Main()
		if not self.d.config.data:
			self.new_credentials = []
			self.ui.text.setText('Введите новый пароль')
			self.ui.btn_enter.clicked.connect(self.one)
		else:
			self.ui.text.setText('Введите пароль от конфига')
			self.ui.btn_enter.clicked.connect(self.simple_unlock)

	def simple_unlock(self):
		if not self.d.config.unlock_file(str(self.ui.input.text())):
			self.ui.text.setText('Неправильный пароль')
		else:
			self.ui.text.setText('Добро пожаловать в Driven!')
			self.w = MainWindow(self.d)
			self.close()
			self.w.show()
		print(self.d.config.data)

	def one(self):
		if self.new_credentials == []:
			self.new_credentials.append(self.ui.input.text())
			self.ui.text.setText('Введите апи токен')
		elif len(self.new_credentials) == 1:
			token = self.ui.input.text()
			self.d.config.get_api(self.ui.input.text())
			if type(self.d.config.api) == vk_api.exceptions.ApiError:
				self.ui.text.setText(f'Неправильный токен {self.d.config.api}')
			else:
				folder_location = os.path.join(os.path.expanduser("~"), confs.FOLDER_NAME)
				self.ui.text.setText(f'Введите директорию. Оставьте поле пустым для {folder_location}')
				self.new_credentials.append(token)
		elif len(self.new_credentials) == 2:
			path = self.ui.input.text()
			if not path:
				path = os.path.join(os.path.expanduser("~"), confs.FOLDER_NAME)
			try:
				os.mkdir(path)
			except FileExistsError:
				pass
			except FileNotFoundError:
				self.ui.text.setText('Неправильный путь. Используется стандартная папка')
				path = os.path.join(os.path.expanduser("~"), confs.FOLDER_NAME)
			self.d.config.new_cfg(token = self.new_credentials[1], password = self.new_credentials[0], dir = path)
			self.d.config.save()
			self.close()

class MainWindow(QMainWindow):

	def __init__(self, d: Driven_Main):
		super(MainWindow, self).__init__()
		self.ui = Ui_Menu()
		self.ui.setupUi(self)
		self.d = d
		self.ui.btn_cfg.clicked.connect(self.edit_config_page)
		self.ui.btn_dialog.accepted.connect(self.config_changed_true)
		self.ui.btn_dialog.rejected.connect(lambda: self.ui.windows_maker.setCurrentIndex(0))

	def edit_config_page(self):
		self.ui.windows_maker.setCurrentIndex(2)
		self.ui.lineEdit_2.setText(self.d.config.data['localdir'])
		self.ui.lineEdit.setText(self.d.config.data['token'])
		self.ui.comboBox_2.clear()
		for archive in self.d.config.data['archives']:
			if self.d.config.data['sync_chat'] == archive['id']:
				item_n = self.d.config.data['archives'].index(archive)
			self.ui.comboBox_2.addItem(archive['name'], archive['id'])
		self.ui.comboBox_2.setCurrentIndex(item_n)

	def config_changed_true(self):
		chat_n = self.ui.comboBox_2.currentIndex()
		if self.ui.lineEdit_2.text() != self.d.config.data['localdir']:
			try:
				os.mkdir(self.ui.lineEdit_2.text())
			except FileExistsError:
				self.ui.info_local.setText(SUCCES_LOCAL)
				self.d.config.data['localdir'] = self.ui.lineEdit_2.text()
			except Exception as err:
				self.ui.info_local.setText(ERROR_LOCATION + str(err))
			else:
				self.ui.info_local.setText(SUCCES_LOCAL)
				self.d.config.data['localdir'] = self.ui.lineEdit_2.text()

		elif self.ui.lineEdit.text() != self.d.config.data['token']:
			self.d.config.get_api(self.ui.lineEdit.text())
			print(self.d.config.api)
			if type(self.d.config.api) == vk_api.exceptions.ApiError:
				self.ui.info_token.setText(ERROR_TOKEN + str(self.d.config.api))
			else:
				self.ui.info_token.setText(SUCCES_TOKEN)
				self.d.config.data['token'] = self.ui.lineEdit.text()

		elif self.d.config.data['archives'][chat_n]['id'] != self.d.config.data['sync_chat']:
			self.d.config.data['sync_chat'] = self.d.config.data['archives'][chat_n]['id']
			self.d.config.data['sync_chat_title'] = self.d.config.data['archives'][chat_n]['name']
			self.d.get_all_versions(self.d.config.data['sync_chat'])
			self.ui.windows_maker.setCurrentIndex(0)
		else:
			self.ui.info_local.setText('<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке</span></p></body></html>')
			self.ui.info_token.setText('<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи</span></p></body></html>')


if __name__ == '__main__':
	app = QApplication(sys.argv)	
	window = Locker()
	window.show()
	sys.exit(app.exec_())