# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : account_views.py
# Time       ：15/12/2021 2:37 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from service import db
from service.models import BLOGUsersModel

from flask.views import MethodView
from flask import jsonify


class HandlerAccountView(MethodView):
    @staticmethod
    def get():
        query = db.session.query(BLOGUsersModel).first()

        print(query.as_dict())
        return jsonify(query)

    @staticmethod
    def post():
        db.session.add(BLOGUsersModel(
            name='admin',
            slug='slug',
            _password='123456',
            email='admin@blog.com'
        ))
        db.session.commit()
        return jsonify([])
