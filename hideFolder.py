#!/usr/bin/python

import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

def unzipdir(file: str):
    with zipfile.ZipFile(file, 'r') as file:
        file.extractall('.')
#if __name__ == '__main__':
#    zipf = zipfile.ZipFile('file.zip', 'w', zipfile.ZIP_DEFLATED)
#    zipdir('secret', zipf)
#    zipf.close()

