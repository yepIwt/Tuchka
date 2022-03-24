import ui_class
import core
import confs
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import os, sys

"""
	Заметка алгоритма.
	Если есть конфиг есть:
		Локер (ввод пароля)
	иначе:
		Локер (новый пароль)
		Логин+Пароль
		Выбор чатов для Архива
	Выбор уже Сохраненных Архивов
	=> Архив Вью
"""

if __name__ == "__main__":
	c = confs.Config()

	if c.config_here:

		# Локер (ввод пароля)
		LockerApp = QtWidgets.QApplication(sys.argv)
		Locker = ui_class.Locker(c)
		Locker.setWindowTitle("Tuchka: Login")
		Locker.setWindowIcon(QtGui.QIcon("ui/Icon.jpg"))
		
		Locker.show()
		LockerApp.exec_()

		ProgramCore = core.DrivenCore(Locker.c)
	else:

		# Локер (новый пароль)
		LockerApp = QtWidgets.QApplication(sys.argv)
		Locker = ui_class.Locker(c)
		Locker.setWindowTitle("Tuchka: Login")
		Locker.setWindowIcon(QtGui.QIcon("ui/Icon.jpg"))
		Locker.show()
		LockerApp.exec_()

		new_passw = Locker.passw

		# Логин+Пароль
		LoginInterfaceApp = QtWidgets.QApplication(sys.argv)
		LoginInterface = ui_class.Registration()
		LoginInterface.show()
		LoginInterfaceApp.exec_()

		cr = LoginInterface.credentials

		# Пока только токены, ребят. Надо писать в саппорт чтобы дали права на права
		token = cr[0] + cr[1]

		c.new_cfg(
			vk_api_token = token,
			new_password = new_passw
		)

		ProgramCore = core.DrivenCore(c)
		AllChats = ProgramCore._get_all_chats()

		# Выбор чатов для Архива
		ListArchivesViewApp = QtWidgets.QApplication(sys.argv)
		Chats = ui_class.ListArchivesView(chats = AllChats)
		Chats.show()
		ListArchivesViewApp.exec_()

		c.data['archives'] = Chats.archives
		for arch in Chats.archives:
			os.mkdir(arch['folder'])
		c.save()

	"""
		Старт программы (MainWindow)
	"""

	assert c.data != None

	# Выбор уже Сохраненных Архивов
	MainApp = QtWidgets.QApplication(sys.argv)
	MainWindow = ui_class.MainWindow(config = c, pcore = ProgramCore)
	MainWindow.setWindowTitle("Tuchka")
	MainWindow.setWindowIcon(QtGui.QIcon("ui/Icon.jpg"))
	MainWindow.show()
	MainApp.exec_()