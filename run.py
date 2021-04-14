#!/usr/bin/python

import os, sys, shutil
import confs
import hideFolder
import zipfile
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime
import requests as r

from PyQt5 import Qt, QtCore, QtWidgets
#uis
import ui

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui.NewRegister.Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
