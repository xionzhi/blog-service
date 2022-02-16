# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : post_views.py
# Time       ：1/1/2022 10:21 下午
# Author     ：xionzhi
# version    ：python 3.9
# Description：
"""

import typing as t

from itertools import groupby

from flask.views import MethodView
from flask import request

from service import db
from service.common.errors import ApiRequestException
from service.common.bolts import success_response

from service.schema import (BLOGPostsTagsSchema, \
                            BLOGUsersSchema,
                            BLOGPostsSchema,
                            )
from service.models import (BLOGUsersModel,
                            BLOGPostsModel,
                            BLOGTagsModel,
                            BLOGPostsTagsModel,
                            )


class HandlerPostDetailView(MethodView):
    @staticmethod
    def get():
        """
        文章查询
        :return:
        """
        _slug: str = request.args.get('slug', None)

        if not _slug:
            raise ApiRequestException(400, 'params error')

        post_query: BLOGPostsModel = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.slug == _slug,
                   BLOGPostsModel.post_status == 'publish').first()

        if not post_query:
            raise ApiRequestException(400, 'params error')

        post_data: dict = BLOGPostsSchema().dump(post_query)

        # query user
        user_query: BLOGUsersModel = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.id == post_query.author_id).first()
        user_data: dict = BLOGUsersSchema().dump(user_query)

        post_data['user_data'] = user_data

        # query tag
        post_tags_query = db.session.query(BLOGPostsTagsModel.tag_id,
                                           BLOGPostsTagsModel.tag_name,
                                           BLOGPostsTagsModel.sort_order). \
            filter(BLOGPostsTagsModel.post_id == post_query.id,
                   BLOGPostsTagsModel.status == 1). \
            order_by(BLOGPostsTagsModel.sort_order.asc()).all()
        post_tags_list = BLOGPostsTagsSchema(many=True).dump(post_tags_query)

        post_data['post_tags_list'] = post_tags_list

        return success_response(data=dict(post_data=post_data))

    @staticmethod
    def post():
        """
        文章新增
        :return:
        """
        _title: str = request.json['title']
        _slug: str = request.json['slug']
        _markdown: str = request.json['markdown']
        _html: str = request.json['html']
        _author_id: int = request.json['author_id']
        _post_status: str = request.json.get('post_status', 'draft')
        _post_tags: list = request.json.get('post_tags', [])

        if db.session.query(BLOGPostsModel.slug).filter(BLOGPostsModel.slug == _slug).first():
            raise ApiRequestException(400, 'unique slug')

        post_query = BLOGPostsModel(
            title=_title,
            slug=_slug,
            markdown=_markdown,
            html=_html,
            post_status=_post_status,
            author_id=_author_id)
        db.session.add(post_query)
        db.session.flush()

        # insert post tags
        if _post_tags:
            post_id = post_query.id
            _ = [{'post_id': post_id, 
                  'tag_id': tag_item['tag_id'], 
                  'tag_name': tag_item['tag_name'], 
                  'sort_order': idx}
                 for idx, tag_item in enumerate(_post_tags)]
            db.session.bulk_insert_mappings(BLOGPostsTagsModel, _)

        db.session.commit()

        post_data: dict = BLOGPostsSchema().dump(post_query)

        return success_response(data=dict(post_data=post_data))

    @staticmethod
    def put():
        """
        文章修改
        """
        _post_id: int = request.json['post_id']
        _title: str = request.json['title']
        _slug: str = request.json['slug']
        _markdown: str = request.json['markdown']
        _html: str = request.json['html']
        _post_tags: list = request.json.get('post_tags', [])  # [{tag_id: 1, tag_name: 'A'}]

        db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.id == _post_id). \
            update({BLOGPostsModel.title: _title,
                    BLOGPostsModel.slug: _slug,
                    BLOGPostsModel.markdown: _markdown,
                    BLOGPostsModel.html: _html})

        if _post_tags:
            # get sort index
            sort_post_tags: dict = {i['tag_id']: i.update(idx=idx) or i for idx, i in enumerate(_post_tags)}
            post_tags_ids: list = list(sort_post_tags.keys())

            # query post_tags
            post_tags_query: t.List[BLOGPostsTagsModel] = db.session.query(BLOGPostsTagsModel). \
                filter(BLOGPostsTagsModel.post_id == _post_id,
                       BLOGPostsTagsModel.status == 1). \
                order_by(BLOGPostsTagsModel.sort_order.asc()).all()
            post_tags_list: list = [i.tag_id for i in post_tags_query]

            if post_tags_list != post_tags_ids:
                # update tags
                for _query in post_tags_query:
                    item: dict = sort_post_tags.get(_query.tag_id)
                    if item:
                        _query.tag_name = item['tag_name']
                        _query.sort_order = item['idx']
                    else:
                        _query.status = 0

                # in _post_tags but not in post_tags_list -> is new = {1, 2, 3}
                new_tags: set = set(post_tags_ids) - set(post_tags_list)
                if new_tags:
                    _ = [{'post_id': _post_id,
                          'tag_id': tag_id,
                          'tag_name': sort_post_tags[tag_id]['tag_name'],
                          'sort_order': sort_post_tags[tag_id]['idx']}
                         for tag_id in new_tags]
                    db.session.bulk_insert_mappings(BLOGPostsTagsModel, _)
        
        db.session.commit()
        return success_response(data=dict())

    @staticmethod
    def patch():
        """
        文章状态
        """
        _post_id: int = request.json['post_id']
        _post_status: str = request.json['post_status']

        db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.id == _post_id). \
            update({BLOGPostsModel.post_status: _post_status})

        db.session.commit()
        return success_response(data=dict())


class HandlerPostListView(MethodView):
    @staticmethod
    def get():
        """
        文章列表
        """
        _tag_id: int = request.args.get('tag_id', 0, int)

        _page: int = request.args.get('page', 1, int)
        _size: int = request.args.get('size', 10, int)

        post_query = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.status == 1,
                   BLOGPostsModel.post_status == 'publish'). \
            order_by(BLOGPostsModel.id.desc())

        if _tag_id:
            post_ids = db.session.query(BLOGPostsTagsModel.post_id). \
                filter(BLOGPostsTagsModel.tag_id == _tag_id,
                       BLOGPostsTagsModel.status == 1).all()
            post_query = post_query. \
                filter(BLOGPostsModel.id.in_([i.post_id for i in post_ids]))

        post_query = post_query.limit(_size).offset((_page - 1) * _size)

        post_list = BLOGPostsSchema(many=True).dump(post_query.all())
        total = post_query.count()

        # update user dict
        user_query = db.session.query(BLOGUsersModel.id,
                                      BLOGUsersModel.name,
                                      BLOGUsersModel.image,
                                      BLOGUsersModel.cover). \
            filter(BLOGUsersModel.id.in_([i['author_id'] for i in post_list])).all()
        user_data_dict = {i.id: BLOGUsersSchema().dump(i) for i in user_query}

        # update tags dict
        tags_query = db.session.query(BLOGPostsTagsModel.tag_id,
                                      BLOGPostsTagsModel.tag_name,
                                      BLOGPostsTagsModel.post_id,
                                      BLOGPostsTagsModel.sort_order). \
            filter(BLOGPostsTagsModel.post_id.in_([i.id for i in post_query]),
                   BLOGPostsTagsModel.status == 1). \
            order_by(BLOGPostsTagsModel.post_id.asc()).all()
        # group by post_id
        tags_list: list = BLOGPostsTagsSchema(many=True).dump(tags_query)
        tags_data_dict = {k: sorted(v, key=lambda x: x.get('sort_order')) 
                          for k, v in groupby(tags_list, key=lambda x: x.get('post_id'))}

        post_list = [i.update(user_data=user_data_dict.get(i['author_id'], {}),
                              post_tags_list=tags_data_dict.get(i['id'], [])) or i for i in post_list]

        return success_response(data=dict(post_list=post_list,
                                          total=total, page=_page, size=_size))
