# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : login_views.py
# Time       ：8/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask.views import MethodView
from flask import request

from service import db, bcrypt
from service.common.bolts import success_response
from service.common.errors import ApiRequestException
from service.models import (BLOGUsersModel)
from service.schema import (BLOGUsersSchema)


class HandlerLoginView(MethodView):
    @staticmethod
    def post():
        _email = request.json['email']
        _password = request.json['password']

        user_query = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.email == _email,
                   BLOGUsersModel.status == 1).first()

        if not user_query:
            raise ApiRequestException(403, 'user error or pwd error')

        if bcrypt.check_password_hash(user_query.passwd, _password) is False:
            raise ApiRequestException(403, 'user error or pwd error')

        # set token
        pass

        # return token and userdata
        pass

        return success_response(data=dict())

