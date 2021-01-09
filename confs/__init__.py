import os
import ast
from .crypt import LetItCrypt
from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000

class Config(object):

    __slots__ = ('crypter','data','api')

    def __init__(self,passw):
        self.crypter = LetItCrypt(passw)
        if not os.path.exists('data'):
            self.new_cfg()
        config_as_str = self.crypter.dec()
        self.data = ast.literal_eval(config_as_str)
        self.get_api(self.data['token'])
    
    def get_api(self,token: str) -> None:
        session = VkApi(token=token)
        self.api = session.get_api()

    def get_archive_title(self,id: int) -> str:
        return self.api.messages.getChat(chat_id = id - PEER_CONST)['title']

    def create_new_archive(self, title: str):
        new_archive_id = self.api.messages.createChat(title=title)
        self.api.messages.send(peer_id=PEER_CONST+new_archive_id,message=SYNC_CODE,random_id=0)
        return new_archive_id

    def get_all_archives(self,token: str) -> list:
        self.get_api(token)
        messages = self.api.messages.search(q=SYNC_CODE,count=100)
        all_archives = []
        if messages:
            for d in messages['items']:
                if d['peer_id'] > PEER_CONST:
                    archive_title = self.get_archive_title(d['peer_id'])
                    all_archives.append({'name': archive_title,'id':d['peer_id'], 'files': []})
        if not all_archives:
            new_title = input('Похоже, что у вас нет доступных архивов. Я создам новый. Введите название: ')
            new_id = self.create_new_archive(new_title)
            all_archives.append({'name':new_title, 'id': PEER_CONST+new_id, 'files': [] })
        return all_archives

    def new_cfg(self):
        token = input('Введите токен для vk_api (kate mobile token): ')
        archives = self.get_all_archives(token)
        new_config = {
            'token': token, 
            'sync_chat':None,
            'archives': archives,
        }
        self.crypter.enc(str(new_config))
    
    def save_in_file(self) -> None:
        self.crypter.enc(str(self.data))
        config_as_str = self.crypter.dec()
        self.data = ast.literal_eval(config_as_str)