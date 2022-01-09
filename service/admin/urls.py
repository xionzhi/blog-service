# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : urls.py
# Time       ：15/12/2021 2:30 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：独立的后台路由
"""

from flask import Blueprint

from service.admin.views.account_views import HandlerAccountView
from service.admin.views.login_views import HandlerLoginView
from service.admin.views.settings_views import HandlerSettingsView


admin_site = Blueprint('admin', __name__, url_prefix='/v1/api/admin')

admin_site.add_url_rule('/account', view_func=HandlerAccountView.as_view('account'))
admin_site.add_url_rule('/login', view_func=HandlerLoginView.as_view('login'))
admin_site.add_url_rule('/settings', view_func=HandlerSettingsView.as_view('settings'))
