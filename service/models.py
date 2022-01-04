# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : models.py
# Time       ：15/12/2021 2:38 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from typing import DefaultDict
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
        return {
            t.name: getattr(self, t.name)
            for t in self.__table__.columns
        }


class BLOGUsersModel(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(254), nullable=False, comment='用户名')
    slug = db.Column(db.String(254), nullable=False, comment='别名')
    password = db.Column(db.String(254), nullable=False, comment='密码')
    email = db.Column(db.String(254), nullable=False, unique=True, index=True, comment='邮箱')
    image = db.Column(db.String(254), comment='图片')
    cover = db.Column(db.String(254), comment='头像')
    bio = db.Column(db.String(254), comment='')
    website = db.Column(db.String(254), comment='网址')
    location = db.Column(db.String(254), comment='位置')
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


class BLOGPostsModel(BaseModel):
    __tablename__ = 'posts'

    title = db.Column(db.String(254), nullable=False, comment='标题')
    slug = db.Column(db.String(254), nullable=False, unique=True, index=True, comment='标题路由')
    markdown = db.Column(db.Text, nullable=False, comment='markdown')
    html = db.Column(db.Text, nullable=False, default='', comment='html')
    image = db.Column(db.String(254), nullable=False, default='', comment='标题图片')
    post_status = db.Column(db.String(254), nullable=False, default='', comment='文章发布状态')
    language = db.Column(db.String(6), comment='语言')
    meta_title = db.Column(db.String(254), comment='')
    meta_description = db.Column(db.String(254), comment='')
    author_id = db.Column(db.Integer, nullable=False, comment='作者ID')


class BLOGTagsModel(BaseModel):
    __tablename__ = 'tags'

    name = db.Column(db.String(254), nullable=False, comment='标签名')
    slug = db.Column(db.String(254), nullable=False, comment='标签别名')


class BLOGPostsTagsModel(BaseModel):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, nullable=False, comment='文章id')
    tag_id = db.Column(db.Integer, nullable=False, comment='标签id')
    sort_order = db.Column(db.Integer, nullable=False, comment='标签排序')
