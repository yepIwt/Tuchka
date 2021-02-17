#!/usr/bin/python
import sys
import confs

from PyQt5.QtCore import QThread, pyqtSignal, QSize
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLineEdit, QPushButton, QWidget, QListWidget, QListWidgetItem, QListView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from uis.ui_main import Ui_MainWindow
from vk_api import exceptions

class FilesWidget(QListWidget):

	def __init__(self):
		super().__init__()
		self.setAcceptDrops(True)
		icon = QIcon('fileicon.png')
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.addItem(QListWidgetItem(icon, 'filename'))
		self.setGridSize(QSize(100,100))
		self.setViewMode(QListView.ViewMode(1))
		

	def dragEnterEvent(self, event):
		event.accept()
		print(event.mimeData().urls())
		#print(event.source().WhatsThis())
		#print(dir(event.mimeData().retrieveData()))

	def dragMoveEvent(self, event):
		event.accept()

	def dropEvent(self, event):
		if event.mimeData().urls():
			event.setDropAction(Qt.CopyAction)
			file_path = event.mimeData().urls()[0].toLocalFile()
			print(file_path)

class MainWindow(QMainWindow, Ui_MainWindow):

	__slots__ = ('config','temp')

	def __init__(self, parent = None, *args, **kwargs):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.winchanger.setCurrentIndex(0)
		self.config = confs.Config()
		self.temp = []
		wid = FilesWidget()
		self.files_layout.addWidget(wid)
		print('Конфиг то есть? - ',self.config.data)
		if not self.config.data:
			self.winchanger.setCurrentIndex(2)
			self.new_config_procedure()
		else:
			self.winchanger.setCurrentIndex(2)
			self.change_quest_page('Enter password')
			self.one_line.clear()
			self.one_line.returnPressed.connect(self.decrypt_config)

	def change_quest_page(self, text):
		self.one_label.setText(text)
		self.one_label.setAlignment(QtCore.Qt.AlignCenter)
		self.one_label.setFont(QtGui.QFont('Cantarell', 26))
		self.one_label.setStyleSheet("font-weight: bold")

	def new_api_check(self, token=None):
		new_api = token or self.one_line.text()
		self.config.get_api(new_api)
		if isinstance(self.config.api, exceptions.ApiError):
			self.change_quest_page(str(self.config.api))
		else:	#Возможна ошибка двойного перезапуска
			self.config.new_cfg(new_api,self.temp[0])
			self.winchanger.setCurrentIndex(1)
			self.config.save()

	def get_new_password(self):
		self.temp.append(self.one_line.text())
		self.change_quest_page('New Api')
		self.one_line.returnPressed.connect(self.new_api_check)

	def new_config_procedure(self):
		self.change_quest_page('New Password')
		self.one_line.returnPressed.connect(self.get_new_password)

	def decrypt_config(self):
		unlocked = self.config.unlock_file(self.one_line.text())
		if unlocked:
			self.change_quest_page('Получение vk-api')
			self.config.get_api(self.config.data['token'])
			self.change_quest_page('Получен vk-api')
			self.winchanger.setCurrentIndex(1)

			#self.files.addItem('test')
			#self.files.addItem('ne test')
			#self.files.setDragDropMode(self.files.InternalMove)
			#print(self.files.setAcceptDrops(True))
		else:
			self.change_quest_page('Bad pasasword')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())