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
from service.models import (BLOGUsersModel,
                            BLOGPostsModel,
                            BLOGTagsModel,
                            BLOGPostsTagsModel)


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
        post_dict: dict = post_query.as_dict()

        user_query: BLOGUsersModel = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.id == post_query.author_id).first()
        user_dict: dict = user_query.as_dict()

        post_dict['user_info'] = user_dict

        return jsonify(dict(code=200, data=post_dict, msg='ok'))

    @staticmethod
    def post():
        """
        文章新增
        :return:
        """
        return jsonify({})
