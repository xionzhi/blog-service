# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：4/1/2022 5:51 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import pytest

from uuid import uuid4

from test import client


client = client

hex_uuid = uuid4().hex


@pytest.fixture()
def user_name():
    return f'测试用户{hex_uuid}'


@pytest.fixture()
def user_slug():
    return f'测试标记{hex_uuid}'


@pytest.fixture()
def user_password():
    return '123456'


@pytest.fixture()
def user_email():
    return f'{hex_uuid}@blog.com'
