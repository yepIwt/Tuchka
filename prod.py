#!/usr/bin/python
import sys
import confs

from PyQt5.QtCore import QThread, pyqtSignal, QSize
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLineEdit, QPushButton, QWidget, QListWidget, QListWidgetItem, QListView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDrag

from uis.ui_main import Ui_MainWindow
from vk_api import exceptions

class FilesWidget(QListWidget):

	def __init__(self):
		super().__init__()
		self.setAcceptDrops(False)
		icon = QIcon('fileicon.png')
		self.addItem(QListWidgetItem(icon, 'filename1'))
		self.addItem(QListWidgetItem(icon, 'filename2'))
		self.addItem(QListWidgetItem(icon, 'filename3'))
		self.addItem(QListWidgetItem(icon, 'filename4'))
		self.addItem(QListWidgetItem(icon, 'filename5'))
		self.addItem(QListWidgetItem(icon, 'filename6'))
		self.addItem(QListWidgetItem(icon, 'filename7'))
		self.addItem(QListWidgetItem(icon, 'filename8'))
		self.addItem(QListWidgetItem(icon, 'filename9'))
		self.addItem(QListWidgetItem(icon, 'filename10'))
		self.addItem(QListWidgetItem(icon, 'filename11'))
		self.addItem(QListWidgetItem(icon, 'filename12'))
		self.addItem(QListWidgetItem(icon, 'filename13'))
		self.addItem(QListWidgetItem(icon, 'filename14'))
		self.addItem(QListWidgetItem(icon, 'filename15'))
		self.addItem(QListWidgetItem(icon, 'filename16'))
		self.addItem(QListWidgetItem(icon, 'filename17'))
		self.addItem(QListWidgetItem(icon, 'secret_photo'))
		self.setGridSize(QSize(100,100))
		self.setViewMode(QListView.ViewMode(1))
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setDropIndicatorShown(True);
		self.setDragDropMode(QAbstractItemView.InternalMove)

	def startDrag(self, actions):
		drag = QtGui.QDrag(self)
		indexes = self.selectedIndexes()
		mime = self.model().mimeData(indexes)
		urlList = []
		for index in indexes:
			urlList.append(QtCore.QUrl.fromLocalFile(index.data()))
		mime.setUrls(urlList)
		drag.setMimeData(mime)
		drag.exec_(actions)
		print(drag.mimeData().urls())
		print(drag.mimedata)

	def dragEnterEvent(self, event):
		event.accept()

	def dragMoveEvent(self, event):
		event.accept()

	def dropEvent(self, event):
		#event.dropAction().as_integer_ratio()
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
		self.setAcceptDrops(True)
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