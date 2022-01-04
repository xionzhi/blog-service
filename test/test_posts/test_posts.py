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
                     post_author_id):
    params = {
        'title': post_title,
        'slug': post_slug,
        'markdown': post_markdown,
        'html': post_html,
        'author_id': post_author_id
    }

    resp = client.post('/v1/api/post/detail', json=params).json
    assert resp['code'] == 200


def test_post_query(client, post_slug):
    params = {
        'slug': post_slug
    }

    resp = client.get('/v1/api/post/detail', query_string=params).json
    assert resp['code'] == 200
