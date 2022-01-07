# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schema.py
# Time       ：4/1/2022 6:52 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""
from service import ma

from service.models import (BLOGUsersModel,
                            BLOGPostsModel,
                            BLOGTagsModel,
                            BLOGPostsTagsModel,
                            )


class BaseSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer()
    uuid = ma.String()
    status = ma.Integer()
    ctime = ma.DateTime(format='%Y-%m-%d %H:%M:%S')
    mtime = ma.DateTime(format='%Y-%m-%d %H:%M:%S')


class BLOGUsersSchema(BaseSchema):
    class Meta:
        model = BLOGUsersModel
        exclude = ['ctime', 'email', 'id', 'last_login', 'mtime', 'password', 'uuid']


class BLOGPostsSchema(BaseSchema):
    class Meta:
        model = BLOGPostsModel


class BLOGTagsSchema(BaseSchema):
    class Meta:
        model = BLOGTagsModel


class BLOGPostsTagsSchema(BaseSchema):
    class Meta:
        model = BLOGPostsTagsModel


class JoinBLOGTagsAndBLOGPostsTags(BLOGTagsSchema, BLOGPostsTagsSchema):
    pass
