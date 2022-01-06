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
from service.models import (DICTPostsTagsModel)


def drop_database():
    db.drop_all()


def create_database():
    db.create_all()


def init_dict_table():
    def dict_post_status():
        _ = [{'post_status': 'draft', 'post_status_cn': 'draft'},
             {'post_status': 'publish', 'post_status_cn': 'publish'}]
        db.session.bulk_insert_mappings(DICTPostsTagsModel, _)

    dict_post_status()
    db.session.commit()


if __name__ == '__main__':
    drop_database()
    create_database()
    init_dict_table()
