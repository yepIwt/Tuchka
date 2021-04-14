import ui
from PyQt5 import Qt, QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui.NewRegister.Ui_MainWindow()
        self.ui.setupUi(self)
