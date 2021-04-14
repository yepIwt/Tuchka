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

from PyQt5 import Qt
#uis
import classes

if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = classes.MainWindow()
    window.show()
    sys.exit(app.exec_())
