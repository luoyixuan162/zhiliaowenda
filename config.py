"""
配置文件
"""


# redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


# mysql数据库配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@127.0.0.1:3306/zhiliaowenda"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 配置密钥
SECRET_KEY = "zxcvbnm"

# flask-mail 配置  --QQ邮箱
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True  # 是否ssl加密
MAIL_DEBUG = True
MAIL_USERNAME = '1902206219@qq.com'
MAIL_PASSWORD = 'vatjxfiojmiecigg'  # 邮箱授权码
MAIL_DEFAULT_SENDER = '1902206219@qq.com'
# MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND = None
# MAIL_ASCII_ATTACHMENTS = False
