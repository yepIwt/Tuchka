from PyQt5 import QtCore, QtWidgets, uic, QtGui
import sys


def create_ui_release_widget(name, commit_name):
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

class Registration(QtWidgets.QMainWindow):


	def __init__(self):
		super(Registration, self).__init__()
		uic.loadUi('ui/FirstRegistration.ui', self)
		self.ExecuteButton.clicked.connect(self.get_credentials)
	
	def get_credentials(self):
		log = self.LoginLine.text()
		passw = self.PasswordLine.text()
		self.credentials = (log, passw)
		self.close()

class ArchiveView(QtWidgets.QWidget):
	
	def __init__(self):
		super(ArchiveView, self).__init__()
		uic.loadUi('ui/ArchiveView.ui', self)
		self.ChatName.setText("Chat Name")
		self.UpButton.clicked.connect(self.go_up)
		self.DownButton.clicked.connect(self.go_down)
		self.SelectButton.clicked.connect(self.go_change_release)

		vlay = QtWidgets.QVBoxLayout()
		wid1 = create_ui_release_widget("Никита Сергиевский", "Привет, мир!")
		wid2 = create_ui_release_widget("Никки Ебланевский", "Гудбай, Америка!")

		vlay.addWidget(wid1); vlay.addWidget(wid2)
		self.ReleasesWidget.setLayout(vlay)
	
	def go_up(self):
		print("Go Up!")

	def go_down(self):
		print("Go Down!")
	
	def go_change_release(self):
		print("Change Release to ... !")

class ListArchivesView(QtWidgets.QWidget):
	
	def __init__(self, allchats, archives = None):
		super(ListArchivesView, self).__init__()
		uic.loadUi('ui/ListArchivesView.ui', self)
		self.chats.clear()
		self.save.clicked.connect(self.get_sel_chats)
		
		if archives:
			self.save.deleteLater()
			self.chats.itemDoubleClicked.connect(self.go_to_archive)
		
		# Добавление чатов в инт
		for (peer_id, chat_title, _) in allchats:
			self.add_chat_to_ui(chat_title, peer_id, archives = archives)
	
	def add_chat_to_ui(self, name, chat_id, archives = None):
		it = QtWidgets.QListWidgetItem(name)
		if not archives:
			it.setFlags(it.flags() | QtCore.Qt.ItemIsUserCheckable)
			it.setCheckState(QtCore.Qt.Unchecked)
		font = QtGui.QFont()
		font.setPointSize(37)
		it.setFont(font)
		it.chat_id = chat_id
		
		self.chats.setMinimumWidth(self.chats.sizeHintForColumn(0))
		self.chats.addItem(it)
	
	def get_sel_chats(self):
		checked_items = []
		for index in range(self.chats.count()):
			if self.chats.item(index).checkState() == QtCore.Qt.Checked:
				checked_items.append(self.chats.item(index))
		
		self.archives = []
		for c in checked_items:
			self.archives.append(c.chat_id)

		self.close()
	
	def go_to_archive(self):
		items = self.chats.selectedItems()[0]
		print(items)
		print(items.chat_id)
		print(items.text())

# QStackedWidget changes pages to (ListArchivesView, ArchiveView, ...)
class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, config, pcore):
		super(MainWindow, self).__init__()
		uic.loadUi('ui/MainWindow.ui', self)

		self.c = config
		self.d = pcore
		
		allarhives = []

		for a in self.c.data['archive_ids']:
			title = self.d._get_chat_title_by_peer_id(a)
			peer_id = a
			allarhives.append(
				(peer_id, title, None)
			)
		

		list_ach = ListArchivesView(allchats = allarhives, archives = True)
		self.pages.addWidget(list_ach)
		
		#sel_ach = ArchiveView()
		#self.pages.addWidget(sel_ach)

		self.pages.setCurrentIndex(1)

class Locker(QtWidgets.QMainWindow):

	def __init__(self, config):
		super(Locker, self).__init__()
		uic.loadUi('ui/Locker.ui', self)
		self.ExecuteButton.clicked.connect(self.enter)
		self.passw = None
		self.c = config

	def enter(self):
		self.passw = self.ConfigPassword.text()

		if not self.c.config_here:
			self.close()
		else:

			unlocked = self.c.open(self.passw)
			if not unlocked:
				self.bad_password()
			else:
				self.close()

	def bad_password(self):
		self.ConfigPassword.setText("")
		self.log_msg.setText("Неправильный пароль")


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = Locker()
	ui.show()
	app.exec_()