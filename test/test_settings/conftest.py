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
def settings_type():
    return 'core'


@pytest.fixture()
def settings_key():
    return 'title'


@pytest.fixture()
def settings_value():
    return f'{hex_uuid}'
