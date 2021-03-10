import os
import ast
from .crypt import LetItCrypt
from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000
FOLDER_NAME = 'DrivenCloud'

class Config(object):

    __slots__ = ('crypter','data','api','is_decrypted')

    def __init__(self):
        self.crypter = None
        if not os.path.exists('data'):
            self.data = False
        else:
            self.data = True

    def unlock_file(self,passw: str) -> bool:
        self.crypter = LetItCrypt(passw)
        try:
            self.data = self.crypter.dec_cfg()
        except:
            pass
        if not self.data:
            return False
        else:
            self.data = ast.literal_eval(self.data)
            return True

    def save(self):
        self.crypter.enc_cfg(str(self.data))

    def get_api(self,token: str) -> None:
        session = VkApi(token=token)
        self.api = session.get_api()
        try:
            self.api.users.get()
        except Exception as error:
            self.api = error

    def get_archive_title(self,id: int) -> str:
        return self.api.messages.getChat(chat_id = id - PEER_CONST)['title']

    def create_new_archive(self, title: str):
        new_archive_id = self.api.messages.createChat(title=title)
        self.api.messages.send(peer_id=PEER_CONST+new_archive_id,message=SYNC_CODE,random_id=0)
        return new_archive_id

    def get_all_archives(self,token: str) -> list:
        #self.get_api(token)
        messages = self.api.messages.search(q=SYNC_CODE,count=100)
        all_archives = []
        if messages:
            for d in messages['items']:
                if d['peer_id'] > PEER_CONST:
                    archive_title = self.get_archive_title(d['peer_id'])
                    all_archives.append({'name': archive_title,'id':d['peer_id']})
        if not all_archives:
            new_id = self.create_new_archive('New Archive')
            all_archives.append({'name':'New Archive', 'id': PEER_CONST+new_id})
        return all_archives

    def new_cfg(self,token,password,dir):
        archives = self.get_all_archives(token)
        if not archives:
            self.api.messages.create_new_archive('Hello World!')
            #archives = self.get_all_archives(token)
            self.new_cfg(token,password,dir)
        new_config = {
            'token': token,
            'sync_chat_title':archives[0]['name'],
            'sync_chat':archives[0]['id'],
            'archives': archives,
            'localdir': dir,
        }
        self.data = new_config
        self.crypter = LetItCrypt(password)