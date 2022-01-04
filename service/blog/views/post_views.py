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


class HandlerPostDetailView(MethodView):
    @staticmethod
    def get():
        """
        文章查询
        :return:
        """
        _slug: str = request.args.get('slug')
        post_data = {
            'title': 'test title',
            'create_time': '2022-01-01',
            'author': 'test user',
            'post_markdown': '## AAA',
            'tags': 'tag1',
            'path': _slug,
        }
        return jsonify(dict(code=200, data=post_data, msg='ok'))

    @staticmethod
    def post():
        """
        文章新增
        :return:
        """
        return jsonify({})
