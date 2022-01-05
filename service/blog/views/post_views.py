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

    @staticmethod
    def put():
        """
        文章修改
        """
        _post_id = request.json['post_id']
        _title = request.json['title']
        _slug = request.json['slug']
        _markdown = request.json['markdown']
        _html = request.json['html']

        db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.id == _post_id). \
            update({BLOGPostsModel.title: _title,
                    BLOGPostsModel.slug: _slug,
                    BLOGPostsModel.markdown: _markdown,
                    BLOGPostsModel.html: _html})
        
        db.session.commit()
        return success_response(data=dict())

    @staticmethod
    def patch():
        """
        文章状态
        """
        _post_id = request.json['post_id']
        _post_status = request.json['post_status']

        db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.id == _post_id). \
            update({BLOGPostsModel.post_status: _post_status})

        db.session.commit()
        return success_response(data=dict())


class HandlerPostListlView(MethodView):
    @staticmethod
    def get():
        """
        文章列表
        """
        _page = request.args.get('page', 1, int)
        _size = request.args.get('size', 10, int)

        post_query = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.status == 1)

        post_query = post_query.limit(_size).offset((_page -1 ) * _size)

        post_list = BLOGPostsSchema(many=True).dump(post_query.all())
        total = post_query.count()

        # update user dict
        pass

        # update tags dict
        pass

        return success_response(data=dict(post_list=post_list,
                                          total=total, page=_page, size=_size))
