

from PyQt5 import QtCore, QtWidgets, uic, QtGui



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