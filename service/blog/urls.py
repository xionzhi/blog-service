# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : urls.py
# Time       ：1/1/2022 10:27 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""
from flask import Blueprint

from service.blog.views.post_views import (HandlerPostDetailView,
                                           HandlerPostListlView)
from service.blog.views.tag_views import (HandlerTagDetailView,
                                          HandlerTagListView)


blog_site = Blueprint('blog', __name__, url_prefix='/v1/api')

blog_site.add_url_rule('/post/detail', view_func=HandlerPostDetailView.as_view('post'))
blog_site.add_url_rule('/post/list', view_func=HandlerPostListlView.as_view('post_list'))
blog_site.add_url_rule('/tag/detail', view_func=HandlerTagDetailView.as_view('tag'))
blog_site.add_url_rule('/tag/list', view_func=HandlerTagListView.as_view('tag_list'))
