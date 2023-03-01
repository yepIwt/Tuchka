
import confs, core, shutil, os
from PyQt5 import QtCore, QtWidgets, uic, QtGui


class Locker(QtWidgets.QMainWidow):
	

	def __init__(self, config: confs.Config):

		# Init frontend
		super(Locker, self).__init__()
		uic.loadUi("screens/Locker.ui", self)

		# Init backend
		self.ExecuteButton.clicked.connect(self.__unlock)
		self.ConfigPassword.setEchoMode(QtWidgets.QLineEdit.Password)  # Активация по Enter
		self._cfg = config
	
	def __unlock(self):
		
		result = self._cfg.open(self.ConfigPassword.text())

		if result:
			self.close()
		else:
			self.locked()
	
	def locked(self):
		self.ConfigPassword.setText("")
		self.log_msg.setText("Пароль не совпадает")


class AppRegistrationMenu(QtWidgets.QMainWindow):


	def __init__(self):

		# Init frontend
		super(AppRegistrationMenu, self).__init__()
		uic.loadUi("screens/Registration.ui", self)
		
		# Init backend
		self.start_btn.clicked.connect(self.__get_token)
	
	def __get_token(self):
		self.credentials = self.PasswordLine.text()
		self.close()


class ListArchivesView(QtWidgets.QMainWindow):
	

	def __init__(self, archives: list = None, chats: list = None):
		
		# Init frontend
		super(ListArchivesView, self).__init__()
		uic.loadUi("screens/ListArchivesView.ui", self)

		# Init backend
		self.save.clicked.connect(self.get_sel_chats)

		if archives:

			self.save.deleteLater()
			self.chats.itemDoubleClicked.connect(self.go_to_archive)

			for (peer_id, chat_title, _, current_release) in archives:
				self.add_archive_to_ui(
					archive_name = chat_title, 
					archive_peer_id = peer_id, 
					curr_rel_unix = current_release
				)
		
		if chats:
			for(peer_id, chat_title, _) in chats:
				self.add_chat_to_ui(
					chat_name = chat_title,
					chat_peer_id = peer_id
				)
	
	def __add_chat_to_frontend(self, chat_name: str, chat_peer_id: int):

		# Создание Item
		frontend_object_chat = QtWidgets.QListWidgetItem(chat_name)
		frontend_object_chat.setFlags(frontend_object_chat.flags() | QtCore.Qt.ItemIsUserCheckable)
		frontend_object_chat.setCheckState(QtCore.Qt.Unchecked)
		frontend_object_chat.peer_id = chat_peer_id

		# Подгонка фронта (что?)
		font = QtGui.QFont(); font.setPointSize(37); frontend_object_chat.setFont(font)

		# Добавление объекта во фронт
		self.chats.addItem(frontend_object_chat)
	
	def __add_archive_to_frontend(self, archive_name: str, archive_peer_id: int, curr_rel_unix: int):
		
		# Создание Item
		archive_in_ui = QtWidgets.QListWidgetItem(archive_name)
		archive_in_ui.peer_id = archive_peer_id
		archive_in_ui.current_release = curr_rel_unix

		# Подгонка фронта (что?)
		font = QtGui.QFont(); font.setPointSize(37); archive_in_ui.setFont(font)

		# Добавление объекта во фронт
		self.chats.setMinimumWidth(self.chats.sizeHintForColumn(0))
		self.chats.addItem(archive_in_ui)
	
	def __get_selected_chats(self):
		
		checked_items = []
		for index in range(self.chats.count()):
			if self.chats.item(index).checkState() == QtCore.Qt.Checked:
				checked_items.append(self.chats.item(index))
		
		self.archives = []
		for chat in checked_items:
			self.archives.append(
				{
					'id': chat.peer_id,
					'folder': str(chat.peer_id),
					'current': "No current",
				}
			)

		# EndPoint
		self.close()
	
	# Для переопределения в будущем
	def go_to_archive_virtual(self, item):
		pass
	
	def go_to_archive(self):
		item = self.chats.selectedItems()[0]
		self.go_to_archive_virtual(item)


class ArchiveSettings(QtWidgets.QWidget):
	

	def __init__(self, chat_id: int, folder_path: str):

		# Init frontend
		super(ArchiveSettings, self).__init__()
		uic.loadUi("screens/ArchiveSettings.ui", self)
		self.FolderPath.setText(folder_path)

		# Init backend
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


class MainWindow(QtWidgets.QMainWindow):
	
	def __init__(self, pcore: core.TuchkaCore):
		
		# Init frontend
		super(MainWindow, self).__init__()
		uic.loadUi("screens/MainWindow.ui", self)

		# Init backend
		self.program_core = pcore

		allarhives = []

		for archive in self.program_core.cfg.data["archives"]:

			title = self.program_core._get_chat_title(archive['id'])
			allarhives.append(
				(archive['id'], title, None, archive['current'])
			)
		
		# Переопределение метода в классе ListArchivesView
		list_ach = ListArchivesView(archives = allarhives)
		list_ach.go_to_archive_virtual = self.open_archive
		self.pages.addWidget(list_ach)

		self.pages.setCurrentIndex(0)
	
	def __find_commits(self, chat_id: int, archive_attachemnts: list):

		result = []

		for fid, unix_time, url_to_file, commit_msg in archive_attachemnts:

			f, l = self.program_core._get_firstlast_name(fid)

			result.append(
				[
					"{} {}".format(f, l), commit_msg, url_to_file, unix_time, chat_id
				]
			)

		return result

	def __save_settings(self, chat_id: int, new_folder_path: str):
		
		# Ищем этот чат среди архивов

		for i in range(len(self.program_core.cfg.data['archives'])):
			if self.d.cfg.data['archives'][i]['id'] == chat_id:
				n = i
				break

		try:
			shutil.rmtree(self.program_core.cfg.data['archives'][n]['folder'])
		except:
			pass

		if not os.access(new_folder_path, os.R_OK):
			os.mkdir(new_folder_path)

		self.program_core.cfg.data['archives'][n]['folder'] = new_folder_path
		self.program_core.cfg.save()

	def __open_settings(self, chat_id: int):

		# Ищем этот чат среди архивов

		n = 0
		for i in range(len(self.program_core.cfg.data['archives'])):

			if self.program_core.cfg.data['archives'][i]['id'] == chat_id:
				n = i
				break
		
		archive = self.program_core.cfg.data['archives'][n]		
		

		self.hwnd = ArchiveSettings(archive['id'], archive['folder'])
		self.hwnd.setWindowTitle("Tuchka: Archive settings")
		self.hwnd.setWindowIcon(QtGui.QIcon("screens/Icon.png"))
		self.hwnd.accept_virtual = self.__save_settings
		self.hwnd.show()
	
	def __update_releases(self, chat_id: int):

		rels = self.program_core._get_history_attachments(chat_id)
		commits = self.__find_commits(chat_id, rels)

		return commits

	def __change_release(self, attachment):

		# Ищем этот чат среди архивов

		for i in range(len(self.d.cfg.data['archives'])):
			if self.d.cfg.data['archives'][i]['id'] == attachment[4]:
				n = i
				break


		# Меняем current на выбранный unixtime

		self.program_core.cfg.data['archives'][n]['current'] = attachment[3]
		self.program_core.cfg.save()

		self.program_core.change_release(
			url_to_file = attachment[2][0],
			folder = self.program_core.cfg.data['archives'][n]['folder']
		)

	def new_release(self, chat_id: int, commit_name: str):

		new_releases, new_current, from_id, url_to_file, commit_message, = self.program_core.synchronization(chat_id, commit_name)

		self.program_core.cfg.data['order'].append(
			(
				from_id,
				new_current,
				url_to_file,
				commit_message
			)
		)

		self.program_core.cfg.save()

		new_releases_with_order, _ = self.d.add_order_to_files(new_releases, self.d.cfg.data['order'])
		
		commits = self.__find_commits(chat_id, new_releases_with_order)
		
		
		return commits, new_current

	
	def open_archive(self, item):
		
		archive_releases = self.program_core._get_history_attachments(item.peer_id)
		commits = self.__find_commits(item.peer_id, archive_releases)

		SelectedArchive = ListArchivesView(item.text(), item.peer_id, item.current_release, commits)
		SelectedArchive.go_change_release_virtual = self.change_release
		SelectedArchive.settings_virtual = self.open_settings_for_chat_id
		SelectedArchive.go_create_release_virtual = self.new_release
		SelectedArchive.update_releases_virtual = self.__update_releases
		self.pages.addWidget(SelectedArchive)

		self.pages.setCurrentIndex(1)