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
from service.models import (DICTPostsTagsModel,
                            BLOGSettingsModel,
                            BLOGTagsModel,
                            DICTTableRowsModel)


def drop_database():
    db.drop_all()


def create_database():
    db.create_all()


def init_dict_table():
    def dict_post_status():
        _ = [{'post_status': 'draft', 'post_status_cn': 'draft'},
             {'post_status': 'publish', 'post_status_cn': 'publish'}]
        db.session.bulk_insert_mappings(DICTPostsTagsModel, _)

    def settings():
        _ = [{'key': 'title', 'value': 'blog title', 'type': 'core'},
             {'key': 'description', 'value': 'blog description', 'type': 'core'},
             {'key': 'language', 'value': 'zh-cn', 'type': 'core'},
             {'key': 'page_size', 'value': '10', 'type': 'blog'},
             {'key': 'is_private', 'value': '0', 'type': 'blog'},
             {'key': 'logo', 'value': '', 'type': 'blog'},
             {'key': 'cover', 'value': '', 'type': 'blog'}]
        db.session.bulk_insert_mappings(BLOGSettingsModel, _)

    def tags():
        _ = [{'name': 'test', 'slug': 'test'}]
        db.session.bulk_insert_mappings(BLOGTagsModel, _)

    def dict_table_rows():
        _ = []
        for table in db.get_tables_for_bind():
            count = db.session.query(table).count()
            _.append({'name': table.name, 'seq': count})
        db.session.bulk_insert_mappings(DICTTableRowsModel, _)

    dict_post_status()
    settings()
    tags()
    dict_table_rows()
    db.session.commit()


if __name__ == '__main__':
    drop_database()
    create_database()
    init_dict_table()
