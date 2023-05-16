# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import os

HOST = '0.0.0.0' # 监听地址
PORT = 5000 # 监听端口
AUTOMATIC = True # 手动部署为False,自动为True

if AUTOMATIC:
    DATABASE = {
        'host': os.environ.get('DATABASE_HOST'),
        'port': os.environ.get('DATABASE_PORT'),
        'username': os.environ.get('DATABASE_USERNAME'),
        'password': os.environ.get('DATABASE_PASSWORD'),
        'name': os.environ.get('DATABASE_NAME'),
        'tablePrefix': os.environ.get('DATABASE_TABLE_PREFIX'),
        'ssl': {
            'caPath': os.environ.get('DATABASE_SSL_CA_PATH'),
            'keyPath': os.environ.get('DATABASE_SSL_KEY_PATH'),
            'certPath': os.environ.get('DATABASE_SSL_CERT_PATH')
        }
    }
else:
    DATABASE = {
        'host': '127.0.0.1', # 数据库地址
        'port': 3306, # 数据库端口
        'username': 'root', # 数据库用户名
        'password': 'root', # 数据库密码
        'name': 'h2o_short_url', # 数据库名称
        'tablePrefix': 'h2o_short_url_', # 数据库表前缀
        'ssl': {
            'caPath': '', # SSL CA路径
            'keyPath': '', # SSL Key路径
            'certPath': '' # SSL Cert路径
        }
    }