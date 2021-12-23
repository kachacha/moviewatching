#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "episode_api.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/23"
__time__ = "15:27:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

from enum import Enum, unique

from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields

from ..config import iqiyi_headers, qq_m_header, youku_headers, youku_m_headers
from ..service.iqiyi_service.crawl import Crawl as IQiYiCrawl
from ..service.qq_service.crawl import Crawl as QqCrawl
from ..service.youku_service.crawl import Crawl as YouKuCrawl

api = Namespace('Episode Api', description='获取视频集数信息接口')


@unique
class Action(Enum):
    DAG = 'dag'
    TASK = 'task'


class Params(fields.Raw):
    def format(self, value):
        return {"params": {}}


class EpisodeModel(Params):

    #  # 链接构造
    @staticmethod
    def get_request():
        get_parser = api.parser()
        get_parser.add_argument('s_type', type=str, help='平台', required=True, default='')
        get_parser.add_argument('page_uri', type=str, help='播放获取集数链接', required=False, default='auto')
        get_parser.add_argument('other', type=int, help='other', required=True, default=1)
        return get_parser

    @staticmethod
    def post_form_request():
        parser = api.parser()
        return parser


@api.route('/episode')
class EpisodeApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iqiyi_crawl = IQiYiCrawl()
        self.qq_crawl = QqCrawl()
        self.youku_crawl = YouKuCrawl()

    @api.expect(EpisodeModel.get_request())
    def get(self):
        s_type = request.args.get('s_type', "qq", str)
        page_uri = request.args.get('page_uri', "", str)
        page = request.args.get('other', 1, int)
        if not page_uri or not s_type:
            return {"code": -100, "message": "fail get episode info. `page_uri` or `s_type` is null."}
        if s_type.__eq__("w_iqiyi") or s_type.__eq__("i_iqiyi"):
            headers = iqiyi_headers
            # html_a_list, page_html = self.iqiyi_crawl.crawl_iqiyi_list(base_url, s_word, headers, page)
        elif s_type.__eq__("qq"):
            headers = qq_m_header
            video_list = self.qq_crawl.crawl_episode(page_uri, headers)
        elif s_type.__eq__("w_youku") or s_type.__eq__("i_youku") or s_type.__eq__("m_youku"):
            headers = youku_m_headers if s_type.__eq__("m_youku") else youku_headers
            # html_a_list, page_html = self.youku_crawl.crawl_youku_list(base_url, s_word, headers, page)
        else:
            return make_response(jsonify({'code': -1, 'message': 'not have search type.'}), 400)
        # if not base_url:
        #     return False

        return {"code": 100, "message": "SUCCESS", "data": video_list} if \
            video_list else {"code": -100, "message": "fail get search page."}

    @api.expect(EpisodeModel.post_form_request())
    @api.doc(params={"action": "方法"})
    def post(self):
        return jsonify({'message': 'successful crawl news.'})
