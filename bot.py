import confs
from vk_api import VkApi
from vk_api import VkUpload

class Base(object):

    __slots__ = ('config')

    def __init__(self,password: str):
        self.config = confs.Config('password')
        if not self.has_sync_chat():
            self.new_sync_chat()
        self.save()

    def new_sync_chat(self) -> None:
        print('Доступные архивы:')
        for a, name in list(enumerate(self.config.data['archives'])):
            print(a, name['name'])
        chat_id = int(input('Выберите чат для синхронизации: '))
        self.config.data['sync_chat'] = self.config.data['archives'][chat_id]['id']
    
    def get_attachments_from(self, archive_id: int):
        # todo: получать больше 200ста файлов
        attachs = self.config.api.messages.getHistoryAttachments(peer_id=archive_id,media_type='doc',count=200)['items']
        attach_json = []
        for attach in attachs:
            attach_json.append({'title':attach['attachment']['doc']['title'], 'link':attach['attachment']['doc']['url']})
        return attach_json

    def has_sync_chat(self) -> bool:
        if not self.config.data['sync_chat']:
            return False
        return True
    
    def upload_file(self, path_to_file: str):
        up = VkUpload(self.config.api)
        new_uploaded_file = up.document(doc = path_to_file)
        file_info = {
            'title': new_uploaded_file['doc']['title'], 
            'link': new_uploaded_file['doc']['url']
        }
        return file_info

    def save(self):
        self.config.save_in_file()

Base('123')