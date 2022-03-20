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
	
	def __init__(self, chat_title, chat_id, attachments):
		super(ArchiveView, self).__init__()
		uic.loadUi('ui/ArchiveView.ui', self)
		self.ChatName.setText(chat_title)
		self.UpButton.clicked.connect(self.go_up)
		self.DownButton.clicked.connect(self.go_down)
		self.SelectButton.clicked.connect(self.go_change_release)
		self.SettingsButton.clicked.connect(self.settings)
		self.chat_id = chat_id

		vlay = QtWidgets.QVBoxLayout()
		for a in attachments:
			wid = create_ui_release_widget(a[0], a[1]  or "(No comment.)")
			wid.url = a[2]
			vlay.addWidget(wid)

		self.ReleasesWidget.setLayout(vlay)
	
	def go_up(self):
		print("Go Up!")

	def go_down(self):
		print("Go Down!")
	
	def go_change_release(self):
		print("Change Release to ... !")
	
	def settings_virtual(self, chat_id):
		pass
	
	def settings(self):
		print("Go to settings!")
		self.settings_virtual(self.chat_id)

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
			self.archives.append(
				{
					'id': c.chat_id,
					'folder': str(c.chat_id)
				}
			)

		self.close()
	
	def go_to_archive_virtual(self, item):
		pass
	
	def go_to_archive(self):
		item = self.chats.selectedItems()[0]
		self.go_to_archive_virtual(item)

class Settings(QtWidgets.QWidget):

	def __init__(self, folder_path):
		super(Settings, self).__init__()
		uic.loadUi('ui/Settings.ui', self)
		self.FolderPath.setText(folder_path)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.new_foolder_path = folder_path
	
	def accept(self):
		self.new_foolder_path = self.FolderPath.text()
		self.close()
	
	def reject(self):
		self.close()


# QStackedWidget changes pages to (ListArchivesView, ArchiveView, ...)
class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, config, pcore):
		super(MainWindow, self).__init__()
		uic.loadUi('ui/MainWindow.ui', self)

		self.c = config
		self.d = pcore
		
		allarhives = []

		for a in self.c.data['archives']:
			title = self.d._get_chat_title_by_peer_id(a['id'])
			peer_id = a['id']
			allarhives.append(
				(peer_id, title, None)
			)
		

		list_ach = ListArchivesView(allchats = allarhives, archives = True)
		list_ach.go_to_archive_virtual = self.open_archive
		self.pages.addWidget(list_ach)

		self.pages.setCurrentIndex(0)

	def open_archive(self, item):
		print(item.text())
		archive_releases = self.d._get_history_attachments_by_peer_id(item.chat_id)
		
		names_and_commits = []
		for fid, _, url_to_file, commit_msg in archive_releases:
			fl = self.d._get_f_l_by_user_id(fid)
			names_and_commits.append(
				[
					fl, commit_msg, url_to_file
				]
			)

		sel_ach = ArchiveView(item.text(), item.chat_id, names_and_commits)
		sel_ach.settings_virtual = self.open_settings_for_chat_id
		self.pages.addWidget(sel_ach)

		self.pages.setCurrentIndex(1)
	
	def open_settings_for_chat_id(self, chat_id):

		n = 0
		for i in range(len(self.c.data['archives'])):
			if self.c.data['archives'][i]['id'] == chat_id:
				n = i
				break
		
		archive = self.c.data['archives'][i]
		hwnd = Settings(archive['folder'])
		hwnd.show()
		print(hwnd.new_foolder_path)

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