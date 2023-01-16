# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from config import HOST, PORT

workers = 5
worker_class = 'gevent'
bind = f'{HOST}:{PORT}'