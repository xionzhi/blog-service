# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : login_views.py
# Time       ：8/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from uuid import uuid4
from flask.views import MethodView
from flask import request

from service import db, cache
from service.common.bolts import (success_response, 
                                  timestamp_now,
                                  bcrypt_checkpw)
from service.common.errors import ApiRequestException
from service.common.wrapper import verify_login
from service.models import (BLOGUsersModel)
from service.schema import (BLOGUsersSchema)


class HandlerLoginView(MethodView):
    @staticmethod
    def post():
        _email: str = request.json['email']
        _password: str = request.json['password']

        user_query = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.email == _email,
                   BLOGUsersModel.status == 1).first()

        if not user_query:
            raise ApiRequestException(400, 'user error or pwd error')

        if bcrypt_checkpw(_password, user_query.password) is False:
            raise ApiRequestException(400, 'user error or pwd error')

        # set token
        token = uuid4().hex
        user_data = BLOGUsersSchema().dump(user_query)
        user_data['token'] = token
        user_data['expired'] = timestamp_now() + 60 * 60
        cache.set(token, user_data, 60 * 60)

        return success_response(data=dict(user_data=user_data))

    @staticmethod
    @verify_login(request)
    def delete():
        _token = request.json['token']

        if not cache.get(_token):
            raise ApiRequestException(400, 'params error')
        cache.delete(_token)

        return success_response(data=dict())

    @staticmethod
    @verify_login(request)
    def put():
        _token = request.json['token']
        _user_data = request.json['user_data']

        if not cache.get(_token):
            raise ApiRequestException(400, 'params error')

        _user_data['expired'] = timestamp_now() + 60 * 60
        cache.set(_token, _user_data, 60 * 60)

        return success_response(data=dict(user_data=_user_data))
        