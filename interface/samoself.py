#!python
import sys
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Slot

@Slot()
def say_hello():
    print("He pressed")

class Form(QDialog):
    
    def __init__(self,parrent=None):
        super(Form, self).__init__(parrent)
        self.setWindowTitle("My Form")
        self.button = QPushButton("Open VKCloud")
        self.button2 = QPushButton("Edit/Show config")
        self.button3 = QPushButton("exit")

        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        
        self.setLayout(self.layout)
        self.button.clicked.connect(self.open_cloud)
        self.button2.clicked.connect(self.open_config)
        self.button3.clicked.connect(self.close_window)

    def open_cloud(self):
        print("He openned cloud")
    
    def open_config(self):
        print("He openned config")

    def close_window(self):
        print("He closed program")
        exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
