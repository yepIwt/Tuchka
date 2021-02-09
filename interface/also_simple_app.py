import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hello World!")
label.show()
app.exec_()

app = QApplication([])
label = QLabel("<font color=red size=40>Hello World!</font>")

