#!/usr/bin/python
import sys
import confs

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLineEdit, QPushButton

from uis.ui_main import Ui_MainWindow
from vk_api import exceptions

class MainWindow(QMainWindow, Ui_MainWindow):

	__slots__ = ('config','temp')

	def __init__(self, parent = None, *args, **kwargs):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.winchanger.setCurrentIndex(0)
		self.config = confs.Config()
		self.temp = []
		print('Конфиг то есть? - ',self.config.data)
		if not self.config.data:
			self.winchanger.setCurrentIndex(2)
			self.new_config_procedure()
		else:
			self.winchanger.setCurrentIndex(2)
			self.change_quest_page('Enter password')
			print('Чето да, вроде есть')
			self.one_line.clear()
			self.one_line.returnPressed.connect(self.decrypt_config)

	def change_quest_page(self, text):
		self.one_label.setText(text)
		self.one_label.setAlignment(QtCore.Qt.AlignCenter)
		self.one_label.setFont(QtGui.QFont('Cantarell', 26))
		self.one_label.setStyleSheet("font-weight: bold")

	def new_api_check(self):
		new_api = self.one_line.text()
		self.config.get_api(new_api)
		if isinstance(self.config.api, exceptions.ApiError):
			self.change_quest_page(str(self.config.api))
		else:	#Возможна ошибка двойного перезапуска
			print('Закрепил с этим паорлем',self.temp[0])
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
		print(f'ДЕкриптинг файлс виф {self.one_line.text()}')
		right = self.config.unlock_file(self.one_line.text())
		print('Здесь же! конфиг - ',self.config.data)
		if right:
			self.change_quest_page('Unlocked!')
		else:
			self.change_quest_page('Bad pasasword')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())