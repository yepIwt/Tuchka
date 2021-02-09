import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QApplication, QFileDialog
from PySide6 import QtUiTools

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
#       QtUiTools.QUiLoader().load("filename.ui")
        QtUiTools.QtUiLoader().load('start_page.ui')
        self.start.clicked.connect(self.start)

    def start(self):
        print("He pressed that button")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    widget = QtWidgets.QstackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(400)
    widget.setFixedHeight(300)
    widget.show()
    sys.exit(app.exec_())



