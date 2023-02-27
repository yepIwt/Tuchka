
import confs
from PyQt5 import QtCore, QtWidgets, uic, QtGui


class Locker(QtWidgets.QMainWidow):
	

	def __init__(self, config: confs.Config):

		# Init frontend
		super(Locker, self).__init__()
		uic.loadUi("screens/Locker.ui", self)

		# Init backend
		self.ExecuteButton.clicked.connect(self.__unlock)
		self.ConfigPassword.setEchoMode(QtWidgets.QLineEdit.Password)  # Активация по Enter
		self._cfg = config
	
	def __unlock(self):
		
		result = self._cfg.open(self.ConfigPassword.text())

		if result:
			self.close()
		else:
			self.locked()
	
	def locked(self):
		self.ConfigPassword.setText("")
		self.log_msg.setText("Пароль не совпадает")


class AppRegistrationMenu(QtWidgets.QMainWindow):


	def __init__(self):

		# Init frontend
		super(AppRegistrationMenu, self).__init__()
		uic.loadUi("screens/Registration.ui", self)
		
		# Init backend
		self.start_btn.clicked.connect(self.__get_token)
	
	def __get_token(self):
		self.credentials = self.PasswordLine.text()
		self.close()