#!/usr/bin/python
import sys
import time
import ast
import confs
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLineEdit, QPushButton

from uis.ui_main import Ui_MainWindow

from bot import Base

def create_password_entry(self):
    self.password = QLineEdit(self.page_load)
    self.password.setObjectName("password")
    self.gridLayout_2.addWidget(self.password, 3, 1, 1, 1)
    self.password.returnPressed.connect(self.try_to_unlock)

def one_question(self, ask, func):
    self.winchanger.setCurrentIndex(3)
    self.new_label.setText(ask)
    self.new_label.setAlignment(QtCore.Qt.AlignCenter)
    self.new_label.setFont(QtGui.QFont('Cantarell', 20))
    self.new_label.setStyleSheet("font-weight: italic")
    self.new_line.returnPressed.connect(func)

class MainWindow(QMainWindow, Ui_MainWindow):

    __slots__ = ('config')

    def __init__(self,parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.winchanger.setCurrentIndex(0)
        self.config = confs.Config()
        print(self.config.data)
        if self.config.data:
            create_password_entry(self)
        else:
            one_question(self, 'New Password', self.create_new_config)

    def create_new_config(self):
        pass

    def try_to_unlock(self):
        self.password.text()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
