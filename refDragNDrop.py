import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class DragTest(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.addItems(['one', 'two', 'three'])
        self.setSelectionMode(self.MultiSelection)

    def startDrag(self, actions):
        drag = QtGui.QDrag(self)
        indexes = self.selectedIndexes()
        mime = self.model().mimeData(indexes)
        urlList = []
        for index in indexes:
            urlList.append(QtCore.QUrl.fromLocalFile(index.data()))
        mime.setUrls(urlList)
        drag.setMimeData(mime)
        drag.exec_(actions)


if __name__ == "__main__":
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    w = DragTest()
    w.show()

    app.exec_()