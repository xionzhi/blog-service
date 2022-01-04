# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : post_views.py
# Time       ：1/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask.views import MethodView
from flask import jsonify, request

from service import db
from service.common.errors import ApiRequestException
from service.common.bolts import success_response

from service.schema import (BLOGUsersSchema,
                            BLOGPostsSchema,
                            )
from service.models import (BLOGUsersModel,
                            BLOGPostsModel,
                            BLOGTagsModel,
                            BLOGPostsTagsModel,
                            )


class HandlerPostDetailView(MethodView):
    @staticmethod
    def get():
        """
        文章查询
        :return:
        """
        _slug: str = request.args.get('slug')

        post_query: BLOGPostsModel = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.slug == _slug).first()

        if not post_query:
            raise ApiRequestException(400, 'params error')

        post_data: dict = BLOGPostsSchema().dump(post_query)

        user_query: BLOGUsersModel = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.id == post_query.author_id).first()
        user_data: dict = BLOGUsersSchema().dump(user_query)

        post_data['user_data'] = user_data

        return success_response(data=dict(post_data=post_data))

    @staticmethod
    def post():
        """
        文章新增
        :return:
        """
        _title = request.json['title']
        _slug = request.json['slug']
        _markdown = request.json['markdown']
        _html = request.json['html']
        _author_id = request.json['author_id']

        post_query = BLOGPostsModel(
            title=_title,
            slug=_slug,
            markdown=_markdown,
            html=_html,
            author_id=_author_id)

        db.session.add(post_query)
        db.session.commit()

        post_data: dict = BLOGPostsSchema().dump(post_query)

        return success_response(data=dict(post_data=post_data))
