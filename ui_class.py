from PyQt5 import QtCore, QtWidgets, uic
import sys


class Registration(QtWidgets.QMainWindow):


	def __init__(self):
		super(Registration, self).__init__()
		uic.loadUi('ui/FirstRegistration.ui', self)
		self.ExecuteButton.clicked.connect(self.get_credentials)
	
	def get_credentials(self):
		log = self.LoginLine.text()
		passw = self.PasswordLine.text()
		self.credentials = (log, passw)
		self.close()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = Registration()
	ui.show()
	app.exec_()
	print(ui.credentials)