# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : urls.py
# Time       ：15/12/2021 2:30 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

from flask import Blueprint

from service.admin.views.account_views import HandlerAccountView


admin_site = Blueprint('admin', __name__, url_prefix='/v1/api/admin')

admin_site.add_url_rule('/account', view_func=HandlerAccountView.as_view('account'))
