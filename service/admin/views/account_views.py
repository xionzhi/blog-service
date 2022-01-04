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
from service.models import (BLOGUsersModel)
from service.schema import (BLOGUsersSchema)
from service.common.errors import ApiRequestException

from flask.views import MethodView
from flask import jsonify, request


class HandlerAccountView(MethodView):
    @staticmethod
    def get():
        _user_id = request.args.get('user_id', 0, str)

        user_query: BLOGUsersModel = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.id == _user_id).first()

        if not user_query:
            raise ApiRequestException(400, 'params error')

        user_data = BLOGUsersSchema().dump(user_query)

        return jsonify(dict(code=200, data=user_data))

    @staticmethod
    def post():
        _name: str = request.json['name']
        _slug: str = request.json['slug']
        _password: str = request.json['password']
        _email: str = request.json['email']

        user_query = BLOGUsersModel(
            name=_name,
            slug=_slug,
            _password=_password,
            email=_email)

        db.session.add(user_query)
        db.session.commit()

        user_data = BLOGUsersSchema().dump(user_query)

        return jsonify(dict(code=200, data=user_data))
