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

class ArchiveView(QtWidgets.QWidget):
	
	def __init__(self):
		super(ArchiveView, self).__init__()
		uic.loadUi('ui/ArchiveView.ui', self)
		self.UpButton.clicked.connect(self.go_up)
		self.DownButton.clicked.connect(self.go_down)
		self.SelectButton.clicked.connect(self.go_change_release)
	
	def go_up(self):
		print("Go Up!")

	def go_down(self):
		print("Go Down!")
	
	def go_change_release(self):
		print("Change Release to ... !")

# QStackedWidget changes pages to (ArchiveView, ...)
class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi('ui/MainWindow.ui', self)
		sel_ach = ArchiveView()
		self.pages.addWidget(sel_ach)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = MainWindow()
	ui.show()
	app.exec_()