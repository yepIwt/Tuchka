import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView
import tempfile
import os

class DelayedMimeData(QtCore.QMimeData):
    def __init__(self):
        super().__init__()
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def retrieveData(self, mime_type: str, preferred_type: QtCore.QVariant.Type):
        for callback in self.callbacks.copy():
            result = callback()
            if result:
                self.callbacks.remove(callback)
        temp = QtCore.QMimeData.retrieveData(self, mime_type, preferred_type)
        return temp


class Widget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.addItems(['one', 'two', 'three', 'four'])
        self.setViewMode(QListView.ViewMode(1))
        self.setSelectionMode(self.MultiSelection)

    def make_file(self):
        pass

    def startDrag(self, actions):
        self.drag = QtGui.QDrag(self)
        names = [item.text() for item in self.selectedItems()]
        #print(names) #namefile
        mime = DelayedMimeData()
        self.path_list = []
        for name in names:
            path = os.path.join(tempfile.gettempdir(), 'DragTest', name + ".txt")
            os.makedirs(os.path.dirname(path), exist_ok=True)

            def write_to_file(path=path, contents=name, widget=self):
                if widget.underMouse():
                    return False
                else:
                    with open(path, 'w') as f:
                        #import time
                        #time.sleep(1)
                        self.make_file()
                        # todo: CURL downloader that compiles rn
                        f.write(contents)
                    return True

            mime.add_callback(write_to_file)

            self.path_list.append(QtCore.QUrl.fromLocalFile(path))
        mime.setUrls(self.path_list.first().ff)
        self.drag.setMimeData(mime)
        self.drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        event.accept()
        print(self.path_list)
        #print(dir(self.drag))
        print(self.drag.event(event))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    app.exec_()