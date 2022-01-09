# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py
# Time       ：15/12/2021 1:57 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import socket

from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='../static')

app.config.from_object('config.develop')
if socket.gethostname() == 'service_name':
    app.config.from_object('config.professional')

app.debug = app.config['APP_DEBUG']
app.config['JSON_AS_ASCII'] = False

app.config.setdefault('SQLALCHEMY_DATABASE_URI', app.config['SQLITE_DATABASE_URL'])

db = SQLAlchemy(app)

ma = Marshmallow(app)

cache = Cache(app)

CORS(app)

logger = app.config['LOGGER']


def init_route():
    """
    init route
    """
    from service.admin.urls import admin_site
    from service.blog.urls import blog_site
    app.register_blueprint(admin_site)
    app.register_blueprint(blog_site)


init_route()
