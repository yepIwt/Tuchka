import ui
import sys
from PyQt5 import Qt, QtCore, QtWidgets

class RegisterForm(QtWidgets.QMainWindow):

    def __init__(self, register_mode: bool, cfg = None):
        super(RegisterForm, self).__init__()
        self.ui = ui.NewRegister.Ui_MainWindow()
        self.ui.setupUi(self)
        self.new_credentials = []
        self.cfg = cfg
        # Нажатие enter
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        if register_mode:
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        else:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.texter.returnPressed.connect(self.unlocker)

    def pressedEnter(self):
        if not self.new_credentials: # Первый enter (ввел пароль)
            self.new_credentials.append(self.ui.texter.text()) # Пароль
            self.ui.texter.clear()
            self.set_helper('Введите токен vk_api')
        elif len(self.new_credentials) == 1: # Ввел токен vk_api
            # ticket: bad token
            self.new_credentials.append(self.ui.texter.text()) # Vk api token
            self.ui.texter.clear()
            self.set_helper('Введите путь до локальной папки')
        elif len(self.new_credentials) == 2: # Ввел токен
            self.new_credentials.append(self.ui.texter.text()) # Путь к папке
            self.ui.texter.clear()
            self.set_helper('Зарегистрированно')
            self.close()

    def set_helper(self, text: str):
        self.ui.texter.setPlaceholderText(text)

    def unlocker(self):
        if not self.cfg.unlock_file(self.ui.texter.text()):
            self.set_helper('Неправильный пароль')
        else:
            self.set_helper('unlocked')
            self.close()
        self.ui.texter.clear()

def start_registration():
    app = Qt.QApplication(sys.argv)
    window = RegisterForm(1)
    window.set_helper('Введите новый пароль')
    window.show()
    app.exec_()
    return tuple(window.new_credentials)

def start_unlocker(config_obj):
    app = Qt.QApplication(sys.argv)
    window = RegisterForm(0, cfg = config_obj)
    window.set_helper('Введите пароль')
    window.show()
    app.exec_()
    return window.cfg
