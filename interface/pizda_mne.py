#!python
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt

class MainWindow(object):

    def __init__(self, obj):
        self.ui = obj
        self.run()

    def show(self):
        self.ui.show()

    def run(self):
        self.ui.loader.setValue(0)
        self.ui.log_loader.setTextFormat(Qt.RichText)
        self.ui.log_loader.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.ui.log_loader.setText("Loading modules")
        print(dir(self.ui.log_loader.timerEvent()))
        self.ui.log_loader.setText("Loaded")
        #self.ui.log_loader("123")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "uis/prod.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    
    win = MainWindow(window)
    win.show()

    sys.exit(app.exec_())
