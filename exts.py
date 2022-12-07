"""
扩展文件
第三方文件，用于存放冲突的模块
"""

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from redis import StrictRedis
import config

db = SQLAlchemy()
mail = Mail()
redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
