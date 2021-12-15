# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : develop.py
# Time       ：15/12/2021 1:56 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import os
import logging.handlers


APP_DEBUG = True

SQL_DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# mysql
DATABASE_HOST = ''
DATABASE_PASSWORD = ''
DATABASE_USER = ''
DATABASE_NAME = ''
DATABASE_PORT = 3306
DATABASE_CHARSET = 'utf8mb4'
MYSQL_DATABASE_URL = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                     f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}' \
                     f'?charset={DATABASE_CHARSET}'

# sqlite
SQLITE_FILE_NAME = 'blog_dev.db'
SQLITE_DATABASE_URL = f'sqlite:///{BASE_DIR}/db/{SQLITE_FILE_NAME}'

# redis
REDIS_HOST = '192.168.191.14'
REDIS_PORT = 6379
REDIS_DB = 2
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# logging
LOG_FILE = f'{BASE_DIR}/log/service.log'
LOGGER_LEVEL = logging.INFO
HANDLER = logging.handlers.TimedRotatingFileHandler(LOG_FILE, 'D', 1, 30)
LOG_FMT = '%(levelname)s %(asctime)s %(pathname)s [line:%(lineno)d] %(message)s'
LOG_FORMATTER = logging.Formatter(LOG_FMT)
HANDLER.setFormatter(LOG_FORMATTER)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(LOGGER_LEVEL)

WEBSITE_HOST = ''
FILE_SERVICE_HOST = ''
