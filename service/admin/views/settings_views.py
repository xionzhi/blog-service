# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : settings_views.py
# Time       ：8/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from itertools import groupby

from flask.views import MethodView
from flask import request

from service import db
from service.common.bolts import success_response
from service.models import (BLOGSettingsModel)
from service.schema import (BLOGSettingsSchema)


class HandlerSettingsView(MethodView):
    @staticmethod
    def get():
        _type = request.args.get('type', None)

        settings_query = db.session.query(BLOGSettingsModel.key,
                                          BLOGSettingsModel.value,
                                          BLOGSettingsModel.type). \
            filter(BLOGSettingsModel.status == 1)

        if _type:
            settings_query = settings_query.filter(BLOGSettingsModel.type == _type)

        settings_query = settings_query.order_by(BLOGSettingsModel.type.asc()).all()

        settings_list = BLOGSettingsSchema(many=True).dump(settings_query)

        settings_data = {k: {i['key']: i['value'] for i in v} 
                         for k, v in groupby(settings_list, key=lambda x: x.get('type'))}

        return success_response(data=dict(settings_list=settings_list, settings_data=settings_data))

    @staticmethod
    def patch():
        _key = request.json['key']
        _value = request.json['value']

        settings_query = db.session.query(BLOGSettingsModel). \
            filter(BLOGSettingsModel.key == _key).first()

        if settings_query:
            settings_query.value = _value
            db.session.commit()

        return success_response(data=dict())
