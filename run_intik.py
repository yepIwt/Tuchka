from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):

	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('ui/FirstRegistration.ui', self)
		self.show()
		self.ExecuteButton.clicked.connect(lambda: exit())

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()