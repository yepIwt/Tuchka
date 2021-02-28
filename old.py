#!/usr/bin/python
import confs
import os
from vk_api import VkUpload

class Main(object):

	__slots__ = ('config')

	def __init__(self):
		self.config = confs.Config()
		if not self.config.data:
			self.new_cfg_handler()
		else:
			self.config.unlock_file('password')
			self.config.get_api(self.config.data['token'])

	def new_cfg_handler(self):
		pass

	def upload_file(self, path_to_file: str):
		print(self.config.api)
		print(type(self.config.api))
		up = VkUpload(self.config.api)
		filename = os.path.basename(path_to_file)
		new_uploaded_file = up.document(doc = path_to_file,title=filename)
		return new_uploaded_file['doc']['owner_id'], new_uploaded_file['doc']['id']

	def get_files_from_conversation(self, conv_id):
		pass

	def get_attachments_from(self, archive_id: int):
        # todo: получать больше 200ста файлов
        attachs = self.config.api.messages.getHistoryAttachments(peer_id=archive_id,media_type='doc',count=200)['items']
        attach_json = []
        for attach in attachs:
            title = attach['attachment']['doc']['title']
            link = attach['attachment']['doc']['url']
            message_id = attach['message_id']
            attach_json.append({'title':title, 'link':link, 'debug_id':message_id})
        return attach_json

    def upload_file_to_archive(self, path_to_file: str, archive_id = None):
        if not archive_id:
            owner_id, file_id = self.upload_file(path_to_file)
            attach = 'doc' + str(owner_id) + '_' + str(file_id)
            self.config.api.messages.send(peer_id = self.config.data['sync_chat'], attachment=attach, random_id = 0)
        self.delete_temp_file(owner_id,file_id)

Main().get_attachments_from(14)
