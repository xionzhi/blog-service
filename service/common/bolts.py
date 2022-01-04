# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bolts.py
# Time       ：16/12/2021 1:51 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask import jsonify, make_response


def success_response(data: dict, code: int=200, msg: str='success'):
    return make_response(jsonify(code=code, data=data, msg=msg), 200)
