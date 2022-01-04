# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py.py
# Time       ：4/1/2022 4:27 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import os
import tempfile

import pytest

from service import app


__all__ = ['client']


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)
