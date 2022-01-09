# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_settings.py
# Time       ：4/1/2022 5:51 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

def test_settings_list(client,
                       settings_type):
    params = {
        'type': settings_type
    }

    resp = client.get('/v1/api/admin/settings', query_string=params).json
    assert resp['code'] == 200


def test_settings_change(client,
                         settings_key,
                         settings_value):
    params = {
        'key': settings_key,
        'value': settings_value,
    }

    resp = client.patch('/v1/api/admin/settings', json=params).json
    assert resp['code'] == 200
