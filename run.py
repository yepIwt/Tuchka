#!/usr/bin/python

import os, sys, shutil
import confs
import hideFolder
import zipfile
import vk_api.exceptions
from vk_api import VkUpload
from datetime import datetime
from time import gmtime, strftime
import requests as r
#uis
import classes
from PyQt5 import Qt

if __name__ == '__main__':
    encrypted_cfg = confs.Config()
    if not encrypted_cfg.data: # Если нет файлика с настройками
        passw, token, directory = classes.start_registration()
        encrypted_cfg.new_cfg(token,passw,directory)
        encrypted_cfg.save()
    else:
        unlocked_cfg = classes.start_unlocker(encrypted_cfg)
        print(unlocked_cfg.data)
