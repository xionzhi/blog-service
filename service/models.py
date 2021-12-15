# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : models.py
# Time       ：15/12/2021 2:38 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from service import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

from uuid import uuid4
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False, default=lambda: uuid4().hex, comment='数据校验UUID')
    status = db.Column(db.Boolean, nullable=False, default=True, comment='逻辑删除状态')
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    mtime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def as_dict(self):
        return {t.name: getattr(self, t.name) for t in self.__table__.columns}


class BLOGUsersModel(BaseModel):
    __tablename__ = 'blog_users'

    name = db.Column(db.String(150), nullable=False, comment='用户名')
    slug = db.Column(db.String(150), nullable=False, comment='别名')
    password = db.Column(db.String(60), nullable=False, comment='密码')
    email = db.Column(db.String(254), nullable=False, unique=True, index=True, comment='邮箱')
    image = db.Column(db.TEXT, comment='图片')
    cover = db.Column(db.TEXT, comment='头像')
    bio = db.Column(db.String(200), comment='')
    website = db.Column(db.TEXT, comment='网址')
    location = db.Column(db.TEXT, comment='位置')
    language = db.Column(db.String(6), comment='语言')
    meta_title = db.Column(db.String(254), comment='')
    meta_description = db.Column(db.String(254), comment='')
    last_login = db.Column(db.DateTime, comment='')

    @hybrid_property
    def _password(self):
        return self.password

    @_password.setter
    def _password(self, pwd):
        self.password = bcrypt.generate_password_hash(pwd, 8)
