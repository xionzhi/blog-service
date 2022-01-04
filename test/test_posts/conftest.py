# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：4/1/2022 7:41 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import os
import tempfile

import pytest

from uuid import uuid4

from service import app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def post_title():
    return 'test post title'


@pytest.fixture
def post_slug():
    return 'test_slug'


@pytest.fixture
def post_markdown():
    return '### markdown\n ```python\n print(1) \n ```'


@pytest.fixture
def post_html():
    return f'test_slug {uuid4().hex}'


@pytest.fixture
def post_author_id():
    return 1
