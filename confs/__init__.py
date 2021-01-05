from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000

class Config(object):
    
    def __init__(self):
        # todo: проверка config.cfg
        pass
    
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
    
    def pad(self,text: bytes) -> bytes:
        while len(text) % 8 != 0:
            text += b' '
        return text

    def encrypt(self,key: str, data: str) -> bytes:
        des = DES.new(key, DES.MODE_ECB)
        encrypted_text = des.encrypt(data.encode('utf-8'))
        print("encrypted: {}".format(encrypted_text))
        self.decrypt(key,encrypted_text)
        #return encrypted_text
    
    def decrypt(self,key: str, data: bytes) -> str:
        des = DES.new(key, DES.MODE_ECB)
        #padded_test = bytes(data, encoding = 'utf-8')
        decrypted = des.decrypt(data)
        print("decrypted: {}",format(decrypted))

    def new_cfg(self):
        token = input('Введите токен для vk_api (kate mobile token)')
        archives = self.get_all_archives(token)
        new_config = {
            'token': token, 
            'sync_chat':None,
            'archives': archives,
        }
        print(new_config)

a = Config()
a.encrypt('12345678',"infoinfo")