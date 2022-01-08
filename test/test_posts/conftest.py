# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：4/1/2022 7:41 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import pytest

from uuid import uuid4
from random import randint

from test import client


client = client


hex_uuid = uuid4().hex


@pytest.fixture
def post_id():
    return 1


@pytest.fixture
def post_tags():
    return [{'tag_id': 1, 'tag_name': 'test1'}, {'tag_id': 2, 'tag_name': 'test2'}]


@pytest.fixture
def update_post_tags():
    return [{'tag_id': 3, 'tag_name': 'test3'}, {'tag_id': 2, 'tag_name': 'test2'}]


@pytest.fixture
def post_status():
    """
    publish or draft
    """
    # return 'publish' if randint(0, 1) else 'draft'
    return 'publish'


@pytest.fixture
def post_title():
    return 'test post title'


@pytest.fixture
def post_slug():
    return f'test_{hex_uuid}'


@pytest.fixture
def post_markdown():
    return '### markdown\n ```python\n print(1) \n ```'


@pytest.fixture
def post_html():
    return f'<h1>{hex_uuid}</h1>'


@pytest.fixture
def post_author_id():
    return 1
