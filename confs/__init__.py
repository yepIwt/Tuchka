import os
from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000

class Config(object):
    
    def __init__(self):
        if os.path.exists('data'):
            config_as_str = self.decrypt(input('Введите пароль: '))
            print(config_as_str)
        else:
            self.new_cfg()
    
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
    
    def pad(self,text):
        while len(text) % 8 != 0:
            text += b' '
        return text

    def encrypt(self,key: str, data: str) -> None:
       des = DES.new(key.encode('utf-8'), DES.MODE_ECB)
       padded_text = self.pad(data.encode('utf-8'))
       encrypted = des.encrypt(padded_text)
       with open('data','wb') as f:
           f.write(encrypted)

    def decrypt(self,key: str) -> str:
        with open('data','rb') as f:
            data = f.read()
        des = DES.new(key.encode('utf-8'), DES.MODE_ECB)
        try:
            decrypted = des.decrypt(data).strip().decode('utf-8')
            return decrypted
        except UnicodeDecodeError:
            print('Неправильный пароль!')
            exit()

    def new_cfg(self):
        token = input('Введите токен для vk_api (kate mobile token): ')
        archives = self.get_all_archives(token)
        new_config = {
            'token': token, 
            'sync_chat':None,
            'archives': archives,
        }
        self.encrypt(input('Введите новый пароль: '),str(new_config))

a = Config()