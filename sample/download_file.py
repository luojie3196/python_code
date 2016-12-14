#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import urllib.request


# reporthook(blocknum, bs, size)
def reporthook(blocknum, bs, size):
    '''''
    blocknum:已经下载的数据块
    bs:数据块的大小
    size:远程文件的大小
   '''
    per = 100.0 * blocknum * bs / size
    if per > 100 :
        per = 100
    print('%.2f%%' % per)

def download_file(url):
    file_name = os.path.basename(url)
    print(os.getcwd() + file_name)
    res = urllib.request.urlretrieve(url, file_name, reporthook)


url = 'https://repo.continuum.io/archive/Anaconda3-4.2.0-Windows-x86_64.exe'
download_file(url)