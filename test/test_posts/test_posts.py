# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_posts.py
# Time       ：4/1/2022 7:41 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""


def test_post_create(client,
                     post_title,
                     post_slug,
                     post_markdown,
                     post_html,
                     post_status,
                     post_author_id,
                     post_tags):
    params = {
        'title': post_title,
        'slug': post_slug,
        'markdown': post_markdown,
        'html': post_html,
        'post_status': post_status,
        'author_id': post_author_id,
        'post_tags': post_tags,
    }

    resp = client.post('/v1/api/post/detail', json=params).json
    assert resp['code'] == 200


def test_post_query(client, post_slug):
    params = {
        'slug': post_slug
    }

    resp = client.get('/v1/api/post/detail', query_string=params).json
    assert resp['code'] == 200


def test_post_change(client,
                     post_id,
                     post_title,
                     post_slug,
                     post_markdown,
                     post_html,
                     update_post_tags):
    params = {
        'post_id': post_id,
        'title': post_title,
        'slug': post_slug,
        'markdown': post_markdown,
        'html': post_html,
        'post_tags': update_post_tags,
    }
    post = client.get('/v1/api/post/detail', query_string=params).json
    assert post['code'] == 200

    params['post_id'] = post['data']['post_data']['id']
    params['slug'] = post['data']['post_data']['slug']

    resp = client.put('/v1/api/post/detail', json=params).json
    assert resp['code'] == 200


def test_post_change_status(client,
                            post_id,
                            post_status):
    params = {
        'post_id': post_id,
        'post_status': post_status
    }

    resp = client.patch('/v1/api/post/detail', json=params).json
    assert resp['code'] == 200


def test_post_query_list(client,
                         page=1,
                         size=10):
    params = {
        'page': page,
        'size': size
    }

    resp = client.get('/v1/api/post/list', query_string=params).json
    assert resp['code'] == 200
