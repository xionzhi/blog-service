# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_users.py
# Time       ：4/1/2022 5:24 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import pytest


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


@pytest.fixture
def test_user_login(client,
                    user_email,
                    user_password):
    params = {
        'password': user_password,
        'email': user_email,
    }

    resp = client.post('/v1/api/admin/login', json=params).json
    assert resp['code'] == 200

    return resp


def test_user_login_update(client,
                           test_user_login):
    params = {
        'token': test_user_login['data']['user_data']['token'],
        'user_data': test_user_login['data']['user_data'],
    }

    resp = client.put('/v1/api/admin/login', json=params).json
    print(resp)
    assert resp['code'] == 200


def test_user_signout(client,
                      test_user_login):
    params = {
        'token': test_user_login['data']['user_data']['token']
    }

    resp = client.delete('/v1/api/admin/login', json=params).json
    assert resp['code'] == 200
