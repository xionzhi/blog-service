# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : create_database_all.py
# Time       ：15/12/2021 4:08 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service import db


def drop_database():
    db.drop_all()


def create_database():
    db.create_all()


if __name__ == '__main__':
    drop_database()
    create_database()
