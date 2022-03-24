from re import M
from unicodedata import name
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import sys


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
	
	def __init__(self, chat_title, chat_id, current, attachments):
		super(ArchiveView, self).__init__()
		uic.loadUi('ui/ArchiveView.ui', self)
		self.ChatName.setText(chat_title)
		self.create_release.clicked.connect(self.go_create_release)
		self.SettingsButton.clicked.connect(self.settings)
		self.UpdateButton.clicked.connect(self.update_releases)
		self.chat_id = chat_id
		self.atchs = attachments
		self.current = current

		self.add_releases_to_ui()

	def create_widget(self, release_title, commit_name, release_unix_time, release_file_url, N): # N - порядковый номер в atchs
		itemN = QtWidgets.QListWidgetItem(); widget = QtWidgets.QWidget()
		widget.setStyleSheet('''
			QWidget{
				border: None; 
				border-bottom: 2px solid white; 
				color: rgba(255, 255, 255, 230); 
				padding-bottom: 1px; 
			}
			QLabel {
				border: None
			};
		''')
		
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		widget.setSizePolicy(sizePolicy)
		
		archive_name_text =  QtWidgets.QLabel(release_title)
		archive_name_text.setStyleSheet("font-family:'Open Sans'; font-size:20px; font-weight:696; color:#ffffff;")
		
		commit_text = QtWidgets.QLabel(commit_name)
		commit_text.setStyleSheet("font-family:'Open Sans'; font-size:35px; font-weight:696; color:#ffffff;")
		
		change_release_btn =  QtWidgets.QPushButton("Сменить")
		change_release_btn.setStyleSheet("QPushButton {border-bottom: 2px solid white; border-right: 2px solid white; font-size:15px; color:#ffffff;}")
		
		if self.current == release_unix_time:
			change_release_btn.setText("Текущий")
			change_release_btn.setDisabled(True)
			change_release_btn.setStyleSheet("QPushButton {border-bottom: 2px solid white; border-right: 2px solid white; font-size:15px; color: red;}")
		
		change_release_btn.clicked.connect(self.go_change_release)
	
		# Meta Data
		change_release_btn.N = N

		widgetLayout = QtWidgets.QHBoxLayout()
		commit_lay = QtWidgets.QVBoxLayout()	
		commit_lay.addWidget(archive_name_text); commit_lay.addWidget(commit_text)
		widgetLayout.addLayout(commit_lay); widgetLayout.addWidget(change_release_btn); widgetLayout.addStretch()

		widget.setLayout(widgetLayout); itemN.setSizeHint(widget.sizeHint())

		return itemN, widget
	
	def update_releases(self):
		self.atchs = self.update_releases_virtual(self.chat_id)
		self.ReleasesWidget.clear()
		self.add_releases_to_ui()

	def update_releases_virtual(self, chat_id):
		pass
	
	def add_releases_to_ui(self):
		for i,rel in enumerate(self.atchs):
			itemN, widget = self.create_widget(
				release_title = rel[0],
				commit_name = rel[1]  or "(No comment.)", 
				release_unix_time = rel[3],
				release_file_url = rel[2],
				N = i,
			)
			self.ReleasesWidget.addItem(itemN)
			self.ReleasesWidget.setItemWidget(itemN, widget)

	@QtCore.pyqtSlot()
	def go_change_release(self):
		button = self.sender()
		self.go_change_release_virtual(self.atchs[button.N])
		self.ReleasesWidget.clear()
		self.current = self.atchs[button.N][3]
		self.add_releases_to_ui()
	
	def go_change_release_virtual(self, attachment):
		pass

	def settings_virtual(chat_id):
		pass
	
	def go_create_release(self):
		new_releases, new_current = self.go_create_release_virtual(self.chat_id, self.release_name.text() or "No comment.")
		self.ReleasesWidget.clear()
		self.atchs = new_releases
		self.current = new_current

		self.add_releases_to_ui()
		

	def go_create_release_virtual(self, chat_id, folder):
		pass
	
	
	def settings(self):
		self.settings_virtual(self.chat_id)

class ListArchivesView(QtWidgets.QWidget):

	"""
		Initialize: 
		1. List to choose archives
		2. List selected archives
		
	"""
	
	def __init__(self, archives = None, chats = None):
		super(ListArchivesView, self).__init__()
		uic.loadUi('ui/ListArchivesView.ui', self)
		self.chats.clear()
		self.save.clicked.connect(self.get_sel_chats)
	
		if archives:
			self.save.deleteLater()
			self.chats.itemDoubleClicked.connect(self.go_to_archive)

			for (peer_id, chat_title, chat_photo, current_release) in archives:
				self.add_archive_to_ui(
					archive_name = chat_title, 
					archive_peer_id = peer_id, 
					curr_rel_unix = current_release
				)

		if chats:
			for(peer_id, chat_title, chat_photo) in chats:
				self.add_chat_to_ui(
					chat_name = chat_title,
					chat_peer_id = peer_id
				)

	def add_chat_to_ui(self, chat_name, chat_peer_id):
		chat_in_ui = QtWidgets.QListWidgetItem(chat_name)
		chat_in_ui.setFlags(chat_in_ui.flags() | QtCore.Qt.ItemIsUserCheckable)
		chat_in_ui.setCheckState(QtCore.Qt.Unchecked)
		font = QtGui.QFont(); font.setPointSize(37); chat_in_ui.setFont(font)
		
		chat_in_ui.peer_id = chat_peer_id
		
		self.chats.setMinimumWidth(self.chats.sizeHintForColumn(0))
		self.chats.addItem(chat_in_ui)

	def add_archive_to_ui(self, archive_name, archive_peer_id, curr_rel_unix):
		archive_in_ui = QtWidgets.QListWidgetItem(archive_name)
		font = QtGui.QFont(); font.setPointSize(37); archive_in_ui.setFont(font)

		archive_in_ui.peer_id = archive_peer_id
		archive_in_ui.current_release = curr_rel_unix

		self.chats.setMinimumWidth(self.chats.sizeHintForColumn(0))
		self.chats.addItem(archive_in_ui)

	def get_sel_chats(self):
		checked_items = []
		for index in range(self.chats.count()):
			if self.chats.item(index).checkState() == QtCore.Qt.Checked:
				checked_items.append(self.chats.item(index))
		
		self.archives = []
		for it in checked_items:
			self.archives.append(
				{
					'id': it.peer_id,
					'folder': str(it.peer_id),
					'current': "No current",
				}
			)

		self.close()

	def go_to_archive_virtual(self, item):
		pass
	
	def go_to_archive(self):
		item = self.chats.selectedItems()[0]
		self.go_to_archive_virtual(item)

class Settings(QtWidgets.QWidget):

	def __init__(self, chat_id, folder_path):
		super(Settings, self).__init__()
		uic.loadUi('ui/Settings.ui', self)
		self.FolderPath.setText(folder_path)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.chat_id = chat_id
		self.new_foolder_path = folder_path
	
	def accept_virtual(self, chat_id, new_folder_name):
		pass
	
	def accept(self):
		self.new_foolder_path = self.FolderPath.text()
		self.accept_virtual(self.chat_id, self.new_foolder_path)
		self.close()
	
	def reject(self):
		self.close()


# QStackedWidget changes pages to (ListArchivesView, ArchiveView, ...)
class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, config, pcore):
		super(MainWindow, self).__init__()
		uic.loadUi('ui/MainWindow.ui', self)

		#self.c = config
		self.d = pcore
		self.d.cfg = config
		
		allarhives = []

		for a in self.d.cfg.data['archives']:
			title = self.d._get_chat_title_by_peer_id(a['id'])
			peer_id = a['id']
			allarhives.append(
				(peer_id, title, None, a['current'])
			)

		list_ach = ListArchivesView(archives = allarhives)
		list_ach.go_to_archive_virtual = self.open_archive
		self.pages.addWidget(list_ach)

		self.pages.setCurrentIndex(0)

	def open_archive(self, item):

		archive_releases = self.d._get_history_attachments_by_peer_id(item.peer_id)
		nms_cms = self.catch_names_and_commits_from_archive_attachments(item.peer_id, archive_releases)

		sel_ach = ArchiveView(item.text(), item.peer_id, item.current_release, nms_cms)
		sel_ach.go_change_release_virtual = self.change_release
		sel_ach.settings_virtual = self.open_settings_for_chat_id
		sel_ach.go_create_release_virtual = self.new_release
		sel_ach.update_releases_virtual = self.update_releases
		self.pages.addWidget(sel_ach)

		self.pages.setCurrentIndex(1)
	
	def update_releases(self, chat_id):
		rels = self.d._get_history_attachments_by_peer_id(chat_id)
		nms = self.catch_names_and_commits_from_archive_attachments(chat_id, rels)
		return nms
	
	def catch_names_and_commits_from_archive_attachments(self, chat_id, archive_attachemnts):
		names_and_commits = []

		for fid, unix_time, url_to_file, commit_msg in archive_attachemnts:
			fl = self.d._get_f_l_by_user_id(fid)
			names_and_commits.append(
				[
					fl, commit_msg, url_to_file, unix_time, chat_id
				]
			)
		return names_and_commits
	
	def open_settings_for_chat_id(self, chat_id):

		n = 0
		for i in range(len(self.d.cfg.data['archives'])):
			if self.d.cfg.data['archives'][i]['id'] == chat_id:
				n = i
				break
		
		archive = self.d.cfg.data['archives'][n]
		
		self.hwnd = Settings(archive['id'], archive['folder'])
		self.hwnd.accept_virtual = self.save_settings
		self.hwnd.show()
	
	def change_release(self, attachment):
		print("Пошла поехала смена релиза", attachment)
		for i in range(len(self.d.cfg.data['archives'])):
			if self.d.cfg.data['archives'][i]['id'] == attachment[4]:
				n = i
				break
		
		#Меняем current на выбранный unixtime
		self.d.cfg.data['archives'][n]['current'] = attachment[3]
		self.d.cfg.save()

		self.d.change_release(
			url_to_file = attachment[2][0],
			folder = self.d.cfg.data['archives'][n]['folder']
		)

	def new_release(self, chat_id, commit_name):

		new_releases, new_current, from_id, url_to_file, commit_message, = self.d.synchronization(chat_id, commit_name)
		self.d.cfg.data['order'].append(
			(
				from_id,
				new_current,
				url_to_file,
				commit_message
			)
		)
		self.d.cfg.save()

		new_releases_with_order, new_order = self.d.add_order_to_files(new_releases, self.d.cfg.data['order'])
		
		names_and_cms = self.catch_names_and_commits_from_archive_attachments(chat_id, new_releases_with_order)
		
		
		return names_and_cms, new_current

	def save_settings(self, chat_id, new_folder_path):
		for i in range(len(self.d.cfg.data['archives'])):
			if self.d.cfg.data['archives'][i]['id'] == chat_id:
				n = i
				break
		self.d.cfg.data['archives'][i]['folder'] = new_folder_path
		self.d.cfg.save()

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
	ui = Settings('sdfsdf')
	ui.show()
	app.exec_()