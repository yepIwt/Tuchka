from PyQt5 import QtWidgets, uic
import sys

def create_message(name, commit_name):
	wid = QtWidgets.QWidget()
	vlay = QtWidgets.QVBoxLayout()

	text1 = QtWidgets.QLabel(name)
	text2 = QtWidgets.QLabel(commit_name)
	text1.setStyleSheet("font-family:'Open Sans'; font-size:20px; font-weight:696; color:#ffffff;")
	text2.setStyleSheet("font-family:'Open Sans'; font-size:35px; font-weight:696; color:#ffffff;")
	
	vlay.addWidget(text1)
	vlay.addWidget(text2)
	
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
	
	wid.setSizePolicy(sizePolicy)
	wid.setLayout(vlay)
	
	wid.setStyleSheet('''
		QWidget{
		border: None; 
		border-bottom: 2px solid white; 
		color: rgba(255, 255, 255, 230); 
		padding-bottom: 1px; }
		QLabel {border: None};
		''')
	
	return wid

class Ui(QtWidgets.QWidget):

	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('ui/ArchiveView.ui', self)
		wid1 = create_message("Никита Сергиевский", 'Коммит')
		wid2 = create_message("Никки Ебланский", 'АнтиКоммит')
		vlay = QtWidgets.QVBoxLayout()
		vlay.addWidget(wid1)
		vlay.addWidget(wid2)

		self.ReleasesWidget.setLayout(vlay)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()