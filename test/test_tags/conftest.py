# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：7/1/2022 9:57 上午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""


import pytest

from uuid import uuid4

from test import client


client = client


hex_uuid = uuid4().hex


@pytest.fixture
def name():
    return f'{hex_uuid}'

