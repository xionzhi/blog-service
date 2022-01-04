# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：4/1/2022 5:51 下午
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


@pytest.fixture()
def user_name():
    return f'测试用户{uuid4().hex}'


@pytest.fixture()
def user_slug():
    return f'测试标记{uuid4().hex}'


@pytest.fixture()
def user_password():
    return '123456'


@pytest.fixture()
def user_email():
    return f'{uuid4().hex}@blog.com'
