# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : wrapper.py
# Time       ：8/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from functools import wraps
from flask import request

from service import cache
from service.common.errors import ApiRequestException


def verify_login(request: request):
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            token = request.environ.get('HTTP_TOKEN')

            if not token:
                raise ApiRequestException(401, 'not permissions')

            _user_data = cache.get(token)

            if not _user_data:
                raise ApiRequestException(403, 'params or token error')

            setattr(request, '_user_data', _user_data)

            return func(*args, **kwargs)
        
        return _wrapper
    return wrapper
