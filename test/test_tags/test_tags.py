# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_tags.py
# Time       ：7/1/2022 9:57 上午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""


def test_tag_create(client,
                    name):
    params = {
        'name': name
    }

    resp = client.post('/v1/api/tag/detail', json=params).json
    assert resp['code'] == 200


def test_tag_delete(client,
                    name):
    params = {
        'tag_id': None,
        'name': name
    }
    tag = client.get('/v1/api/tag/detail', query_string={'name': name}).json
    assert tag['code'] == 200

    params['tag_id'] = tag['data']['tag_data']['id']

    resp = client.delete('/v1/api/tag/detail', json=params).json
    assert resp['code'] == 200


def test_post_query_list(client,
                         name):
    params = {
        'keyword': name
    }

    resp = client.get('/v1/api/tag/list', query_string=params).json
    assert resp['code'] == 200
