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
from flask import jsonify, request

from service import db
from service.common.errors import ApiRequestException
from service.common.bolts import success_response


class HandlerTagDetailView(MethodView):
    @staticmethod
    def get():
        """
        标签查询
        :return:
        """
        pass

    @staticmethod
    def post():
        """
        标签新增
        :return:
        """
        pass

    @staticmethod
    def put():
        """
        标签修改
        :return:
        """
        pass

    @staticmethod
    def delete():
        """
        标签删除
        :return:
        """
        pass


class HandlerTagListView(MethodView):
    @staticmethod
    def get():
        """
        标签列表
        :return:
        """
        pass
