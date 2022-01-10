# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tag_views.py
# Time       ：5/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask.views import MethodView
from flask import request

from service import db
from service.common.errors import ApiRequestException
from service.common.bolts import success_response
from service.models import (BLOGTagsModel,
                            BLOGPostsTagsModel)
from service.schema import (BLOGTagsSchema)


class HandlerTagDetailView(MethodView):
    @staticmethod
    def get():
        _name: str = request.args.get('name', None)

        if not _name:
            raise ApiRequestException(400, 'params error')

        tag_query = db.session.query(BLOGTagsModel). \
            filter(BLOGTagsModel.name == _name).first()

        tag_data = BLOGTagsSchema().dump(tag_query)

        return success_response(data=dict(tag_data=tag_data))

    @staticmethod
    def post():
        """
        标签新增
        :return:
        """
        _name: str = request.json['name']

        if db.session.query(BLOGTagsModel.name).filter(BLOGTagsModel.name == _name).first():
            raise ApiRequestException(400, 'unique name')

        tag_query = BLOGTagsModel(
            name=_name,
            slug=_name)

        db.session.add(tag_query)
        db.session.commit()

        tag_data = BLOGTagsSchema().dump(tag_query)

        return success_response(data=dict(tag_data=tag_data))

    @staticmethod
    def delete():
        """
        标签删除
        :return:
        """
        _tag_id: int = request.json['tag_id']
        _name: str = request.json['name']

        # update tags
        db.session.query(BLOGTagsModel). \
            filter(BLOGTagsModel.id == _tag_id,
                   BLOGTagsModel.name == _name). \
            update({BLOGTagsModel.status: 0})

        # update post_tags
        db.session.query(BLOGPostsTagsModel). \
            filter(BLOGPostsTagsModel.tag_id == _tag_id). \
            update({BLOGPostsTagsModel.status: 0})

        db.session.commit()

        return success_response(data=dict())


class HandlerTagListView(MethodView):
    @staticmethod
    def get():
        """
        标签列表
        :return:
        """
        _keyword: str = request.args.get('keyword', None, str)

        tag_query = db.session.query(BLOGTagsModel). \
            filter(BLOGTagsModel.status == 1)

        if _keyword:
            tag_query = tag_query.filter(BLOGTagsModel.name.like(f'%{_keyword}%'))

        tag_list = BLOGTagsSchema(many=True).dump(tag_query.all())

        return success_response(data=dict(tag_list=tag_list))
