# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : errors.py
# Time       ：15/12/2021 4:10 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import traceback

from flask import jsonify
from werkzeug.exceptions import HTTPException

from service import logger, app


class ApiRequestException(HTTPException):
    """
    错误异常捕获
    """
    code = 400
    description = None

    def __init__(self, code, description=None):
        """
        :param code:
        :param description:
        """
        if isinstance(code, ApiRequestException):
            code, description = code.code, code.description

        super(ApiRequestException, self).__init__(code, description)
        self.code = code or self.code
        self.description = description or self.description


@app.errorhandler(Exception)
def all_exception_handler(error):
    """
    response error
    """
    if isinstance(error, ApiRequestException):
        return jsonify({'msg': f'{error.description}', 'code': error.code, 'data': None}), 200

    elif isinstance(error, HTTPException):
        return jsonify({'msg': f'{error.description}', 'code': error.code, 'data': None}), error.code

    logger.error(traceback.format_exc())
    if app.debug is True:
        print(traceback.format_exc())

    return jsonify({'msg': '服务器内部错误', 'code': 500, 'data': None}), 200
