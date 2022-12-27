# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import re

def isUrl(text):
    re_ = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
    return bool(re_.search(text))

def base62Encode(number):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if number == 0:
        return alphabet[0]
    infos = []
    base = len(alphabet)
    while number:
        rem = number % base
        number = number // base
        infos.append(alphabet[rem])
    infos.reverse()
    return ''.join(infos)