from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidget, QApplication, QWidget, QVBoxLayout

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        self.listA = ListWidget(self)
        self.listB = QListWidget(self)
        self.listB.viewport().installEventFilter(self)
        for widget in (self.listA, self.listB):
            widget.setAcceptDrops(True)
            widget.setDragEnabled(True)
            for item in 'One Two Three Four Five Six'.split():
                widget.addItem(item)
            layout.addWidget(widget)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Drop and
            source is self.listB.viewport()):
            self.listB.dropEvent(event)
            if event.isAccepted():
                print('eventFilter', self.listB.count())
            return True
        return QMainWindow.eventFilter(self, source, event)

class ListWidget(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)

    def dropEvent(self, event):
        QListWidget.dropEvent(self, event)
        if event.isAccepted():
            print('dropEvent', self.count())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
