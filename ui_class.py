from PyQt5 import QtCore, QtWidgets, uic, QtGui
import sys


def create_ui_release_widget(name, commit_name):
	wid = QtWidgets.QWidget()
	vlay = QtWidgets.QVBoxLayout()

	text1 = QtWidgets.QLabel(name)
	text2 = QtWidgets.QLabel(commit_name)
	text1.setStyleSheet("font-family:'Open Sans'; font-size:20px; font-weight:696; color:#ffffff;")
	text2.setStyleSheet("font-family:'Open Sans'; font-size:35px; font-weight:696; color:#ffffff;")
	btn = QtWidgets.QPushButton("Press me!")
	
	vlay.addWidget(text1)
	vlay.addWidget(text2)
	vlay.addWidget(btn)
	
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
		QPushButton {border: 2px solid black};
		''')
	
	return wid

def create_ui_release_widget2(name, commit_name, unixtime, url_to_release, func, chat_id, current = False):
	itemN = QtWidgets.QListWidgetItem() 

	widget = QtWidgets.QWidget()
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

	widgetText =  QtWidgets.QLabel(name)
	widgetText.setStyleSheet("font-family:'Open Sans'; font-size:20px; font-weight:696; color:#ffffff;")

	widgetText3 = QtWidgets.QLabel(commit_name)
	widgetText3.setStyleSheet("font-family:'Open Sans'; font-size:35px; font-weight:696; color:#ffffff;")

	widgetButton =  QtWidgets.QPushButton("Сменить")
	widgetButton.setStyleSheet("QPushButton {border-bottom: 2px solid white; border-right: 2px solid white; font-size:15px; color:#ffffff;}")

	if current:
		widgetButton.setText("Текущий")
		widgetButton.setDisabled(True)
		widgetButton.setStyleSheet("QPushButton {border-bottom: 2px solid white; border-right: 2px solid white; font-size:15px; color: red;}")
	

	widgetButton.clicked.connect(func)
	# Meta Data
	widget.unixtime = unixtime
	widget.url = url_to_release
	widget.chat_id = chat_id

	widgetLayout = QtWidgets.QHBoxLayout()
	
	commit_lay = QtWidgets.QVBoxLayout()
	
	commit_lay.addWidget(widgetText)
	commit_lay.addWidget(widgetText3)

	widgetLayout.addLayout(commit_lay)
	widgetLayout.addWidget(widgetButton)
	widgetLayout.addStretch()

	#widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
	widget.setLayout(widgetLayout)  
	itemN.setSizeHint(widget.sizeHint())    

	#Add widget to QListWidget funList
	return itemN, widget


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
		
		self.SettingsButton.clicked.connect(self.settings)
		self.chat_id = chat_id
		self.atchs = attachments
		self.current = current

		vlay = QtWidgets.QVBoxLayout()
		for a in attachments:
			flag = False
			if a[3] == self.current:
				flag = True

			itemN, widget = create_ui_release_widget2(a[0], a[1]  or "(No comment.)", a[3], a[2], func = self.go_change_release, chat_id = a[4], current = flag)
			self.ReleasesWidget.addItem(itemN)
			self.ReleasesWidget.setItemWidget(itemN, widget)

	@QtCore.pyqtSlot()
	def go_change_release(self):
		button = self.sender()
		n = self.ReleasesWidget.indexAt(button.pos()).row()
		self.go_change_release_virtual(self.atchs[n])
	
	def go_change_release_virtual(self, attachment):
		pass
	
	def settings_virtual(self, chat_id):
		pass
	
	def settings(self):
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
		for (peer_id, chat_title, _, current_unix) in allchats:
			self.add_chat_to_ui(chat_title, peer_id, current_unix, archives = archives)
	
	def add_chat_to_ui(self, name, chat_id, current_unix, archives = None):
		it = QtWidgets.QListWidgetItem(name)
		if not archives:
			it.setFlags(it.flags() | QtCore.Qt.ItemIsUserCheckable)
			it.setCheckState(QtCore.Qt.Unchecked)
		font = QtGui.QFont()
		font.setPointSize(37)
		it.setFont(font)
		it.chat_id = chat_id
		it.current = current_unix
		
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
					'folder': str(c.chat_id),
					'current': None,
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

		self.c = config
		self.d = pcore
		
		allarhives = []

		for a in self.c.data['archives']:
			title = self.d._get_chat_title_by_peer_id(a['id'])
			peer_id = a['id']
			allarhives.append(
				(peer_id, title, None, a['current'])
			)
		

		list_ach = ListArchivesView(allchats = allarhives, archives = True)
		list_ach.go_to_archive_virtual = self.open_archive
		self.pages.addWidget(list_ach)

		self.pages.setCurrentIndex(0)

	def open_archive(self, item):

		archive_releases = self.d._get_history_attachments_by_peer_id(item.chat_id)
		
		names_and_commits = []
		for fid, unix_time, url_to_file, commit_msg in archive_releases:
			fl = self.d._get_f_l_by_user_id(fid)
			names_and_commits.append(
				[
					fl, commit_msg, url_to_file, unix_time, item.chat_id
				]
			)

		sel_ach = ArchiveView(item.text(), item.chat_id, item.current, names_and_commits)
		sel_ach.go_change_release_virtual = self.change_release
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
		
		self.hwnd = Settings(archive['id'], archive['folder'])
		self.hwnd.accept_virtual = self.save_settings
		self.hwnd.show()
	
	def change_release(self, attachment):
		print("Пошла поехала смена релиза", attachment)

	
	def save_settings(self, chat_id, new_folder_path):
		for i in range(len(self.c.data['archives'])):
			if self.c.data['archives'][i]['id'] == chat_id:
				n = i
				break
		self.c.data['archives'][i]['folder'] = new_folder_path
		self.c.save()

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