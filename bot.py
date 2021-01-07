import confs
from vk_api import VkApi

class Base(object):

    __slots__ = ('api','config')

    def __init__(self,password: str):
        self.config = confs.Config('password')
        if not self.has_sync_chat():
            self.new_sync_chat()
    
    def new_sync_chat(self) -> None:
        print('Доступные архивы:')
        for a, name in list(enumerate(self.config.data['archives'])):
            print(a, name['name'])
        chat_id = int(input('Выберите чат для синхронизации: '))
        self.config.data['sync_chat'] = self.config.data['archives'][chat_id]['id']
    
    def has_sync_chat(self) -> bool:
        if not self.config.data['sync_chat']:
            return False
        return True
    
    def save(self):
        self.config.save_in_file()

Base('123').save()