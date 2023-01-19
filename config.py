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
        'host': '121.4.52.251',
        'port': 3306,
        'username': 'h2o_short_url',
        'password': 'xhxd6Fip7ZcdhmG4',
        'name': 'h2o_short_url',
        'prefix': 'h2o_short_url_',
        'ssl': {
            'caPath': '',
            'keyPath': '',
            'certPath': ''
        }
    }