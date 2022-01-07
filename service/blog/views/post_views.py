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

from flask.views import MethodView
from flask import request

from service import db
from service.common.errors import ApiRequestException
from service.common.bolts import success_response

from service.schema import (BLOGUsersSchema,
                            BLOGPostsSchema,
                            JoinBLOGTagsAndBLOGPostsTags,
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
            raise ApiRequestException('401', 'params error')

        post_query: BLOGPostsModel = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.slug == _slug).first()

        if not post_query:
            raise ApiRequestException(400, 'params error')

        post_data: dict = BLOGPostsSchema().dump(post_query)

        # query user
        user_query: BLOGUsersModel = db.session.query(BLOGUsersModel). \
            filter(BLOGUsersModel.id == post_query.author_id).first()
        user_data: dict = BLOGUsersSchema().dump(user_query)

        post_data['user_data'] = user_data

        # query tag join post
        post_join_tags_query = db.session.query(BLOGPostsTagsModel.tag_id,
                                                BLOGPostsTagsModel.sort_order,
                                                BLOGTagsModel.name,
                                                BLOGTagsModel.slug,). \
            join(BLOGTagsModel, BLOGTagsModel.id == BLOGPostsTagsModel.tag_id). \
            filter(BLOGPostsTagsModel.post_id == post_query.id,
                   BLOGPostsTagsModel.status == 1). \
            order_by(BLOGPostsTagsModel.sort_order.asc()).all()
        post_tags_list = JoinBLOGTagsAndBLOGPostsTags(many=True).dump(post_join_tags_query)

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
            raise ApiRequestException(401, 'unique slug')

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
            _ = [{'post_id': post_id, 'tag_id': tag_id, 'sort_order': idx}
                 for idx, tag_id in enumerate(_post_tags)]
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
        _post_tags: list = request.json.get('post_tags', [])

        db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.id == _post_id). \
            update({BLOGPostsModel.title: _title,
                    BLOGPostsModel.slug: _slug,
                    BLOGPostsModel.markdown: _markdown,
                    BLOGPostsModel.html: _html})

        if _post_tags:
            # get sort index
            sort_post_tags: dict = {i: idx for idx, i in enumerate(_post_tags)}

            # query post_tags
            post_tags_query: t.List[BLOGPostsTagsModel] = db.session.query(BLOGPostsTagsModel). \
                filter(BLOGPostsTagsModel.post_id == _post_id,
                       BLOGPostsTagsModel.status == 1). \
                order_by(BLOGPostsTagsModel.sort_order.asc()).all()
            post_tags_list: list = [i.tag_id for i in post_tags_query]

            if post_tags_list != _post_tags:
                # update tags
                for _query in post_tags_query:
                    idx = sort_post_tags.get(_query.tag_id, 0)
                    if idx:
                        _query.sort_order = idx
                    else:
                        _query.status = 0

                # in _post_tags but not in post_tags_list -> is new
                new_tags = set(_post_tags) - set(post_tags_list)
                if new_tags:
                    _ = [{'post_id': _post_id,
                          'tag_id': tag_id,
                          'sort_order': sort_post_tags.get(tag_id)}
                         for idx, tag_id in enumerate(new_tags)]
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
        _page: int = request.args.get('page', 1, int)
        _size: int = request.args.get('size', 10, int)

        post_query = db.session.query(BLOGPostsModel). \
            filter(BLOGPostsModel.status == 1,
                   BLOGPostsModel.post_status == 'publish'). \
            order_by(BLOGPostsModel.id.desc())

        post_query = post_query.limit(_size).offset((_page - 1) * _size)

        post_list = BLOGPostsSchema(many=True).dump(post_query.all())
        total = post_query.count()

        # update user dict
        user_query = db.session.query(BLOGUsersModel.id,
                                      BLOGUsersModel.name,
                                      BLOGUsersModel.image,
                                      BLOGUsersModel.cover). \
            filter(BLOGUsersModel.id.in_([i['author_id'] for i in post_list])).all()
        user_data_list = BLOGUsersSchema(many=True).dump(user_query)
        user_data_dict = {i.id: i for i in user_data_list}

        # update tags dict
        post_ids = [i['id'] for i in post_list]
        tags_query = db.session.query(BLOGPostsTagsModel.tag_id,
                                      BLOGPostsTagsModel.post_id,
                                      BLOGTagsModel.name). \
            join(BLOGTagsModel, BLOGPostsTagsModel.id == BLOGPostsTagsModel.tag_id). \
            filter(BLOGPostsTagsModel.post_id.in_(post_ids),
                   BLOGPostsTagsModel.status == 1). \
            order_by(BLOGPostsTagsModel.sort_order.asc()).all()
        # group by post_id
        pass

        return success_response(data=dict(post_list=post_list,
                                          total=total, page=_page, size=_size))
