# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_users.py
# Time       ：4/1/2022 5:24 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""


def test_user_create(client,
                     user_name,
                     user_slug,
                     user_password,
                     user_email):
    params = {
        'name': user_name,
        'slug': user_slug,
        'password': user_password,
        'email': user_email,
    }

    resp = client.post('/v1/api/admin/account', json=params).json

    assert resp['code'] == 200


def test_user_query(client):
    params = {
        'user_id': 1
    }

    resp = client.get('/v1/api/admin/account', query_string=params).json

    assert resp['code'] == 200
    assert resp['data']['id'] == params['user_id']
