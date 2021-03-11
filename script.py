#!/usr/bin/python

import os, sys, shutil
import confs
import hideFolder
import zipfile
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime
import time
import requests as r
# QT
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialogButtonBox
from PyQt5.QtCore import QFile
from ui.locker import Ui_Locker
from ui.mainwindow import Ui_Menu

CHAT_CONST = 2000000000
ERROR_LOCATION = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке: </span><span style=" font-size:20pt; font-weight:600; color:#ff0000;">Ошибка</span></p></body></html>'
SUCCES_LOCAL = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке: </span><span style=" font-size:20pt; font-weight:600; color:#00ff08;">Успех</span></p></body></html>'
ERROR_TOKEN = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи: </span><span style=" font-size:20pt; font-weight:600; color:#ff0000;">Ошибка</span></p></body></html>'
SUCCES_TOKEN = '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи: </span><span style=" font-size:20pt; font-weight:600; color:#00ff08;">Успех</span></p></body></html>'


class Driven_Main(object):

    __slots__ = ('config', 'versions')

    def __init__(self):
        self.config = confs.Config()
        self.versions = []

    def upload_file(self, path):
        up = VkUpload(self.config.api)
        filename = os.path.basename(path)
        new_uploaded_file = up.document(doc=path, title=filename)
        return new_uploaded_file['doc']['owner_id'], new_uploaded_file['doc']['id']

    def load_file_to_conv(self, owner_id, file_id, chat_id):
        if chat_id < CHAT_CONST:
            chat_id += CHAT_CONST
        msg = f'Container: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}'
        self.config.api.messages.send(peer_id=chat_id, message=msg, attachment=f'doc{owner_id}_{file_id}', random_id=0)

    def get_all_versions(self, chat_id):
        if chat_id < CHAT_CONST:
            chat_id += CHAT_CONST
        if not self.versions:
            self.config.get_api(self.config.data['token'])
            attacs = self.config.api.messages.getHistoryAttachments(peer_id=chat_id, media_type='doc', count=200)
            for att in attacs['items']:
                message = self.config.api.messages.getById(message_ids=att['message_id'])
                file_url = message['items'][0]["attachments"][0]['doc']["url"]
                version = message['items'][0]['text'].split('Container: ')[-1]
                #datetime.strptime('2021-03-01 01:32:23', '%Y-%m-%d %H:%M:%S')
                self.versions.append([version, file_url])
        return self.versions

    def sync(self, step: int):
        if step == 1:
            # step1: archive secret to decrypted.zip
            zipf = zipfile.ZipFile('decrypted.zip', 'w', zipfile.ZIP_DEFLATED)
            hideFolder.zipdir(self.config.data['localdir'], zipf)
            zipf.close()
        elif step == 2:
            # step2: encrypt decrypted.zip to container
            self.config.crypter.enc_file()
        elif step == 3:
            # step3: send container
            ow, fi = self.upload_file('container')
            self.load_file_to_conv(ow, fi, 14)
        elif step == 4:
            # step4: delete old file
            os.remove('decrypted.zip')

    def change_version(self, n: int, step: int):
        link = self.versions[n][-1]
        if step == 1:
            # step1: download new container
            file_in_url = r.get(link)
            with open('containerNEW', 'wb') as f:
                f.write(file_in_url.content)
        elif step == 2:
            # step2: umount container
            shutil.rmtree(self.config.data['localdir'])
        elif step == 3:
            # step3: delete secret and container
            os.remove(os.path.join(os.path.dirname(__file__), 'container'))
        elif step == 4:
            # step4: rename containers
            os.rename('containerNEW', 'container')
        elif step == 5:
            # step5: unlock container
            self.config.crypter.dec_file()
        elif step == 6:
            # step6: unzip decrypted.zip
            hideFolder.unzipdir('decrypted.zip', os.path.join(os.path.dirname(self.config.data['localdir']), ''))
        elif step == 7:
            # step7: delete decrypted.zip
            os.remove(os.path.join(os.path.dirname(__file__), 'decrypted.zip'))

class Locker(QMainWindow):

    __slots__ = ('d', 'new_credentials')

    def __init__(self):
        super(Locker, self).__init__()
        self.ui = Ui_Locker()
        self.ui.setupUi(self)
        self.w = None
        self.d = Driven_Main()
        if not self.d.config.data:
            self.new_credentials = []
            self.ui.text.setText('Введите новый пароль')
            self.ui.btn_enter.clicked.connect(self.one)
        else:
            self.ui.text.setText('Введите пароль от конфига')
            self.ui.btn_enter.clicked.connect(self.simple_unlock)

    def simple_unlock(self):
        if not self.d.config.unlock_file(str(self.ui.input.text())):
            self.ui.text.setText('Неправильный пароль')
        else:
            self.ui.text.setText('Добро пожаловать в Driven!')
            self.d.config.get_api(self.d.config.data['token'])
            self.d.config.get_all_archives(self.d.config.data['token'])
            self.w = MainWindow(self.d)
            self.close()
            self.w.show()
        print(self.d.config.data)

    def one(self):
        if self.new_credentials == []:
            self.new_credentials.append(self.ui.input.text())
            self.ui.text.setText('Введите апи токен')
        elif len(self.new_credentials) == 1:
            token = self.ui.input.text()
            self.d.config.get_api(self.ui.input.text())
            if type(self.d.config.api) == vk_api.exceptions.ApiError:
                self.ui.text.setText(f'Неправильный токен {self.d.config.api}')
            else:
                folder_location = os.path.join(
                    os.path.expanduser("~"), confs.FOLDER_NAME)
                self.ui.text.setText(f'Введите директорию. Оставьте поле пустым для {folder_location}')
                self.new_credentials.append(token)
        elif len(self.new_credentials) == 2:
            path = self.ui.input.text()
            if not path:
                path = os.path.join(os.path.expanduser("~"), confs.FOLDER_NAME)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            except FileNotFoundError:
                self.ui.text.setText('Неправильный путь. Используется стандартная папка')
                path = os.path.join(os.path.expanduser("~"), confs.FOLDER_NAME)
            self.d.config.new_cfg(token=self.new_credentials[1], password=self.new_credentials[0], dir=path)
            self.d.config.save()
            self.close()

class MainWindow(QMainWindow):

    def __init__(self, d: Driven_Main):
        super(MainWindow, self).__init__()
        self.ui = Ui_Menu()
        self.ui.setupUi(self)
        self.d = d
        self.ui.btn_cfg.clicked.connect(self.edit_config_page)
        self.ui.btn_sync.clicked.connect(self.sync_process)
        self.ui.btn_change_version.clicked.connect(self.change_version_prepare)
        self.ui.btn_dialog.accepted.connect(self.config_changed_true)
        self.ui.btn_dialog.rejected.connect(lambda: self.ui.windows_maker.setCurrentIndex(0))

    def edit_config_page(self):
        self.ui.windows_maker.setCurrentIndex(2)
        self.ui.lineEdit_2.setText(self.d.config.data['localdir'])
        self.ui.lineEdit.setText(self.d.config.data['token'])
        self.ui.comboBox_2.clear()
        for archive in self.d.config.data['archives']:
            if self.d.config.data['sync_chat'] == archive['id']:
                self.item_n = self.d.config.data['archives'].index(archive)
            self.ui.comboBox_2.addItem(archive['name'], archive['id'])
        self.ui.comboBox_2.setCurrentIndex(self.item_n)

    def config_changed_true(self):
        chat_n = self.ui.comboBox_2.currentIndex()
        if self.ui.lineEdit_2.text() != self.d.config.data['localdir']:
            try:
                os.mkdir(self.ui.lineEdit_2.text())
            except FileExistsError:
                self.item_nineEdit.text() != self.d.config.data['token']
            self.d.config.get_api(self.ui.lineEdit.text())
            if type(self.d.config.api) == vk_api.exceptions.ApiError:
                self.ui.info_token.setText(
                    ERROR_TOKEN + str(self.d.config.api))
            else:
                self.ui.info_local.setText('<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Путь к локальной папке</span></p></body></html>')
                self.ui.info_token.setText('<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">Токен вк-апи</span></p></body></html>')
        elif chat_n != self.item_n:
            self.d.config.data['sync_chat'] = self.d.config.data['archives'][chat_n]['id']
            self.d.config.data['sync_chat_title'] = self.d.config.data['archives'][chat_n]['name']
            self.d.config.save()

    def sync_process(self):
        self.ui.loadbar.setValue(0)
        self.ui.status_line.setText('')
        self.ui.windows_maker.setCurrentIndex(1)
        self.ui.status_line.setText('Syncing...')

        self.ui.status_line.setText('Archiving secret to decrypted.zip')
        self.d.sync(1)
        self.ui.loadbar.setValue(25)

        self.ui.status_line.setText('Encrypting decrypted.zip to container')
        self.d.sync(2)
        self.ui.loadbar.setValue(50)

        self.ui.status_line.setText('Sending container')
        self.d.sync(3)
        self.ui.loadbar.setValue(75)

        self.ui.status_line.setText('Deleting old file')
        self.d.sync(4)
        self.ui.loadbar.setValue(100)
        self.ui.windows_maker.setCurrentIndex(0)

    def change_version_prepare(self):
        if not self.ui.comboBox.count():
            for vers in self.d.get_all_versions(self.d.config.data['sync_chat']):
                self.ui.comboBox.addItem(vers[0], vers[1])
        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.change_version_process)
        self.ui.buttonBox.rejected.connect(lambda: self.ui.windows_maker.setCurrentIndex(0))
        self.ui.windows_maker.setCurrentIndex(3)

    def changing_version(self, vers_n: int):
        self.ui.status_line.setText('')
        self.ui.loadbar.setValue(0)
        self.ui.windows_maker.setCurrentIndex(1)
        self.ui.status_line.setText('Download new container')
        self.d.change_version(vers_n,1)
        self.ui.loadbar.setValue(15)

        self.ui.status_line.setText('Umount container')
        self.d.change_version(vers_n,2)
        self.ui.loadbar.setValue(30)

        self.ui.status_line.setText('Delete secret and container')
        self.d.change_version(vers_n,3)
        self.ui.loadbar.setValue(45)

        self.ui.status_line.setText('Rename containers')
        self.d.change_version(vers_n,4)
        self.ui.loadbar.setValue(60)

        self.ui.status_line.setText('Unlock container')
        self.d.change_version(vers_n,5)
        self.ui.loadbar.setValue(75)

        self.ui.status_line.setText('Unzip decrypted.zip')
        self.d.change_version(vers_n,6)
        self.ui.loadbar.setValue(90)

        self.ui.status_line.setText('Delete decrypted.zip')
        self.d.change_version(vers_n,7)
        self.ui.loadbar.setValue(100)

    def change_version_process(self):
        vers_n = self.ui.comboBox.currentIndex()
        if not self.d.config.data['currentVersion']:
            self.d.config.data['currentVersion'] = self.d.versions[vers_n]
            self.d.config.save()
            self.changing_version(vers_n)
        if self.d.config.data['currentVersion'][0] == self.d.versions[vers_n][0]:
            self.ui.windows_maker.setCurrentIndex(0)
        else:
            self.changing_version(vers_n)
            self.d.config.data['currentVersion'] = self.d.versions[vers_n]
            self.ui.windows_maker.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Locker()
    window.show()
    sys.exit(app.exec_())