import os

AUTOMATIC = True # 手动部署为False,自动为True

HTTP = {
    'host': '0.0.0.0', # HTTP地址
    'port': 478, # HTTP端口
    'ssl': {
        'enable': False, # 启用HTTP SSL
        'keyPath': '', # HTTP SSL Key路径
        'certPath': '' # HTTP SSL Cert路径
    }
}

DATABASE = {
    'host': os.environ.get('DATABASE_HOST') or 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com', # 数据库地址
    'port': int(os.environ.get('DATABASE_PORT', '3306')) or 4000, # 数据库端口
    'username': os.environ.get('DATABASE_USERNAME') or '2nxmQMdzz7M77Sf.root', # 数据库用户名
    'password': os.environ.get('DATABASE_PASSWORD') or '4NWwHgMQNQafvuQw', # 数据库密码
    'name': os.environ.get('DATABASE_NAME') or 'url-database', # 数据库名称
    'tablePrefix': os.environ.get('DATABASE_TABLE_PREFIX') or 'wuyuan_', # 数据库表前缀
    'ssl': {
        'enable': os.environ.get('DATABASE_SSL_ENABLE') or False, # 启用数据库SSL
        'caPath': os.environ.get('DATABASE_SSL_CA_PATH') or '', # 数据库SSL CA路径
        'keyPath': os.environ.get('DATABASE_SSL_KEY_PATH') or '', # 数据库SSL Key路径
        'certPath': os.environ.get('DATABASE_SSL_CERT_PATH') or '' # 数据库SSL Cert路径
    }
}