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
        return {
            t.name: getattr(self, t.name)
            for t in self.__table__.columns
        }


class BLOGUsersModel(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(254), nullable=False, comment='用户名')
    slug = db.Column(db.String(254), nullable=False, comment='别名')
    password = db.Column(db.String(254), nullable=False, comment='密码')
    email = db.Column(db.String(254), nullable=False, comment='邮箱')
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

    __table_args__ = (db.Index('users_email_IDX', 'email', unique=True),
                      db.Index('users_name_IDX', 'name', unique=True), )


class BLOGPostsModel(BaseModel):
    __tablename__ = 'posts'

    title = db.Column(db.String(254), nullable=False, comment='标题')
    slug = db.Column(db.String(254), nullable=False, comment='标题路由')
    markdown = db.Column(db.Text, nullable=False, comment='markdown')
    html = db.Column(db.Text, nullable=False, default='', comment='html')
    image = db.Column(db.String(254), nullable=False, default='', comment='标题图片')
    post_status = db.Column(db.String(254), nullable=False, default='draft', comment='文章发布状态')
    language = db.Column(db.String(6), comment='语言', default='zh-cn')
    meta_title = db.Column(db.String(254), comment='')
    meta_description = db.Column(db.String(254), comment='')
    author_id = db.Column(db.Integer, nullable=False, comment='作者ID')

    __table_args__ = (db.Index('posts_slug_status_IDX', 'slug', 'status', unique=True), )


class BLOGTagsModel(BaseModel):
    __tablename__ = 'tags'

    name = db.Column(db.String(254), nullable=False, comment='标签名')
    slug = db.Column(db.String(254), nullable=False, comment='标签别名')

    __table_args__ = (db.Index('tags_name_status_IDX', 'name', 'status', unique=True), )


class BLOGPostsTagsModel(BaseModel):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, nullable=False, comment='文章id')
    tag_id = db.Column(db.Integer, nullable=False, comment='标签id')
    tag_name = db.Column(db.String(254), nullable=False, comment='标签名')
    sort_order = db.Column(db.Integer, nullable=False, comment='标签排序')

    __table_args__ = (db.Index('posts_tags_post_id_IDX', 'post_id'),
                      db.Index('posts_tags_tag_id_IDX', 'tag_id'),)


class BLOGSettingsModel(BaseModel):
    __tablename__ = 'settings'

    key = db.Column(db.String(254), nullable=False, comment='设置key')
    value = db.Column(db.String(254), nullable=False, comment='设置value')
    type = db.Column(db.String(254), nullable=False, comment='blog core')


class DICTTableRowsModel(BaseModel):
    """
    maybe in redis or memory?
    """
    __tablename__ = 'dict_table_rows'

    name = db.Column(db.String(254), nullable=False, comment='表名')
    seq = db.Column(db.Integer, nullable=False, comment='行数量')


class DICTPostsTagsModel(BaseModel):
    """
    draft 草稿
    publish 发布
    """
    __tablename__ = 'dict_post_status'

    post_status = db.Column(db.String(254), nullable=False, comment='文章发布状态')
    post_status_cn = db.Column(db.String(254), nullable=False, comment='文章发布状态')
