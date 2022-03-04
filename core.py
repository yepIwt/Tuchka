#!/usr/bin/python

"""
    Driven (Tuchka) program core
    yepIwt, 2022
"""

import vk_api
import confs

def get_vk_api(login: str = None, password: str = None, token: str = None):
    
    vk_session = vk_api.VkApi(
        login = login,
        password = password,
        token = token
    )

    api = vk_session.get_api()

    try:
        api.wall.get()
    except Exception as err:
        return False, err
    else:
        return True, api

class DrivenCore:

    _cfg = None

    def __init__(self, config: confs.Config):
        pass

    def _get_all_chats(self):
        pass
    
    def _search_chat_by_title(self):
        pass

    def _get_chat_picture(self):
        pass
    
    def _get_attachments_history(self):
        pass

    def _upload_file(self):
        pass

    def _change_release(self):
        pass

if __name__ == "__main__":
    c = confs.Config()
    if c._config_here:
        unlocked = False
        while unlocked != True:
            password = input("Enter password: ")
            unlocked = c.open(password)
        print("Done!")
    else:
        status = False
        while status != True:
            api_token = input("Enter VK API token: ")
            status, err = get_vk_api(token = api_token)
            if not status:
                print(err)
        new_password = input("Enter new password: ")
        c.new_cfg(api_token, new_password)
        print("Done!")