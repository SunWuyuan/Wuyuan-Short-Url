# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import os

HOST = '0.0.0.0'
PORT = 5000
AUTOMATIC = True #手动部署为False,自动为True

if AUTOMATIC:
    DATABASE = {
        'host': os.environ.get('DATABASE_HOST'),
        'port': os.environ.get('DATABASE_PORT'),
        'username': os.environ.get('DATABASE_USERNAME'),
        'password': os.environ.get('DATABASE_PASSWORD'),
        'name': os.environ.get('DATABASE_NAME'),
        'prefix': os.environ.get('DATABASE_PREFIX'),
        'ssl': {
            'caPath': os.environ.get('DATABASE_SSL_CA_PATH'),
            'keyPath': os.environ.get('DATABASE_SSL_KEY_PATH'),
            'certPath': os.environ.get('DATABASE_SSL_CERT_PATH')
        }
    }
else:
    DATABASE = {
        'host': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'root',
        'name': 'db',
        'prefix': 'h2o_short_url_',
        'ssl': {
            'caPath': '',
            'keyPath': '',
            'certPath': ''
        }
    }