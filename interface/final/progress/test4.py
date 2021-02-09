import sys
import time
import random
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QBasicTimer

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.progressBar = QProgressBar(self)
		self.progressBar.setGeometry(30, 40, 200, 25)
		
		self.btnStart = QPushButton('Start', self)
		self.btnStart.move(40, 80)
		self.btnStart.clicked.connect(self.startProgress)

		self.timer = QBasicTimer()
		self.step = 0

	def startProgress(self):
		if self.timer.isActive():
			self.timer.stop()
			self.btnStart.setText("Start")
		else:
			self.timer.start(100, self)
			self.btnStart.setText('Stop')


	def load_modules(self):
		time.sleep(1)
		self.progressBar.setValue(50)

	def load_vk(self):
		time.sleep(2)
		self.progressBar.setValue(100)

	def timerEvent(self, event):
		if self.progressBar.value() >= 100:
			self.timer.stop()
			self.btnStart.stop()
			return
		self.load_modules()
		self.load_vk()
	#WORKING
		
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	MainWindow = Window()
	MainWindow.show()
	sys.exit(app.exec_())