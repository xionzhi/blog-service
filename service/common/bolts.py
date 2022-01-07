# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bolts.py
# Time       ：16/12/2021 1:51 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask import jsonify, make_response, Response


def success_response(data: dict, code: int = 200, msg: str = 'success') -> Response:
    if 200 >= code <= 299:
        code = 200
    return make_response(jsonify(code=code, data=data, msg=msg), code)
