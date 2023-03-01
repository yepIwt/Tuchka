
import confs
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
		uic.loadUi('screens/ListArchivesView.ui', self)

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
