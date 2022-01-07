# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conftest.py
# Time       ：7/1/2022 9:57 上午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""


import os
import tempfile

import pytest

from uuid import uuid4
from random import randint

from service import app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


hex_uuid = uuid4().hex


@pytest.fixture
def name():
    return f'{hex_uuid}'

