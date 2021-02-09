import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui
#from PyQt5.QtCore import SIGNAL
#from PyQt5.QtGui import QApplication, QMainWindow, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_main import Ui_MainWindow


class Loading(QThread):
	reportProgress = pyqtSignal(int, list)
	calculationFinished = pyqtSignal()

	def __init__(self, numDollars, currentLines):
		super().__init__()
		self.num


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self,parent=None, *args, **kwargs):
		QMainWindow.__init__(self)
		self.setupUi(self)
		#print(dir(self.project_name.setText('123')))
		print(dir(self.progress_bar.setValue(100)))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
