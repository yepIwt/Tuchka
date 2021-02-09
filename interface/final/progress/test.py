from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QTextEdit, QInputDialog, QPushButton, QVBoxLayout, QProgressBar)
import sys


class DollarCalculation(QThread):
    reportProgress = pyqtSignal(int, list)
    calculationFinished = pyqtSignal()

    def __init__(self, numDollars, currentLines):
        super().__init__()

        self.numDollars = numDollars
        self.currentLines = currentLines

    def run(self) -> None:
        for dollar_counter in range(1, self.numDollars + 1):
            word = '$' * dollar_counter
            self.reportProgress.emit(dollar_counter + 1, [word + text for text in self.currentLines])

        self.calculationFinished.emit()


class Tbx(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.dollarCalculation = None

    def initUI(self):
        self.vbox = QVBoxLayout()
        self.btn = QPushButton('ClickMe', self)
        self.btn.clicked.connect(self.dollar)
        self.te = QTextEdit(self)
        self.prgb = QProgressBar(self)
        self.vbox.addWidget(self.te)
        self.vbox.addWidget(self.btn)
        self.vbox.addWidget(self.prgb)
        self.setLayout(self.vbox)
        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Application')


    def dollar(self):
        text_1_int, ok = QInputDialog.getInt(self, 'HowMany?', 'Enter How Many dollar do you want ?')
        if not ok:
            return

        self.btn.setEnabled(False)

        self.prgb.setMaximum(text_1_int + 1)
        self.dollarCalculation = DollarCalculation(text_1_int, self.te.toPlainText().split('\n'))
        self.dollarCalculation.reportProgress.connect(self.progress)
        self.dollarCalculation.calculationFinished.connect(self.calculationFinished)
        self.dollarCalculation.start()

    def progress(self, value, newLines):
        self.te.append('\n'.join(newLines))
        self.prgb.setValue(value)


    def calculationFinished(self):
        self.btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tbx()
    ex.show()
    sys.exit(app.exec_())