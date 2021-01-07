import os
import ast
import crypt
from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000

class Config(object):

    __slots__ = ('crypter','data')

    def __init__(self,passw):
        self.crypter = crypt.LetItCrypt(passw)
        if not os.path.exists('data'):
            self.new_cfg()
        config_as_str = self.crypter.dec()
        self.data = ast.literal_eval(config_as_str)
    
    def get_all_archives(self,token: str) -> list:
        session = VkApi(token=token)
        api = session.get_api()
        messages = api.messages.search(q=SYNC_CODE,count=100)
        all_archives = []
        if messages:
            for d in messages['items']:
                if d['peer_id'] > PEER_CONST:
                    all_archives.append({'name':'todo','id':d['peer_id']})
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