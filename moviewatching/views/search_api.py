#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "search_api.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/10"
__time__ = "19:35:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

from enum import Enum, unique

from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields

from ..config import iqiyi_base_search_url, iqiyi_more_search_url, qq_base_search_url, qq_more_search_url, \
    iqiyi_headers, qq_headers, iqiyi_m_header, iqiyi_m_search, qq_m_header, qq_m_search, youku_base_search_url, \
    youku_more_search_url, youku_headers, youku_m_headers
from ..service.iqiyi_service.crawl import Crawl as IQiYiCrawl
from ..service.qq_service.crawl import Crawl as QqCrawl
from ..service.youku_service.crawl import Crawl as YouKuCrawl

api = Namespace('Search Api', description='获取视频搜索信息接口')


@unique
class Action(Enum):
    DAG = 'dag'
    TASK = 'task'


class Params(fields.Raw):
    def format(self, value):
        return {"params": {}}


class SearchModel(Params):

    #  # 链接构造
    @staticmethod
    def get_request():
        get_parser = api.parser()
        get_parser.add_argument('s_type', type=str, help='搜索平台', required=True, default='')
        get_parser.add_argument('s_word', type=str, help='搜索关键词', required=False, default='auto')
        get_parser.add_argument('page', type=int, help='页数', required=True, default=1)
        return get_parser

    @staticmethod
    def post_form_request():
        parser = api.parser()
        return parser


@api.route('/search')
class SearchApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iqiyi_crawl = IQiYiCrawl()
        self.qq_crawl = QqCrawl()
        self.youku_crawl = YouKuCrawl()

    @api.expect(SearchModel.get_request())
    def get(self):
        s_type = request.args.get('s_type', "qq", str)
        s_word = request.args.get('s_word', "", str)
        page = request.args.get('page', 1, int)
        if s_type.__eq__("w_iqiyi") or s_type.__eq__("i_iqiyi"):
            base_url = iqiyi_more_search_url if page > 1 else iqiyi_base_search_url
            headers = iqiyi_headers
            html_a_list, page_html = self.iqiyi_crawl.crawl_iqiyi_list(base_url, s_word, headers, page)
        elif s_type.__eq__("m_iqiyi"):
            base_url = iqiyi_m_search
            headers = iqiyi_m_header
            html_a_list, page_html = self.iqiyi_crawl.crawl_m_iqiyi_list(base_url, s_word, headers)
        elif s_type.__eq__("w_qq") or s_type.__eq__("i_qq"):
            base_url = qq_more_search_url if page > 1 else qq_base_search_url
            headers = qq_headers
            html_a_list, page_html = self.qq_crawl.crawl_qq_list(base_url, s_word, headers, page)
        elif s_type.__eq__("m_qq"):
            base_url = qq_m_search
            headers = qq_m_header
            html_a_list, page_html = self.qq_crawl.crawl_m_qq_list(base_url, s_word, headers)
        elif s_type.__eq__("w_youku") or s_type.__eq__("i_youku") or s_type.__eq__("m_youku"):
            base_url = youku_more_search_url if page > 1 else youku_base_search_url
            headers = youku_m_headers if s_type.__eq__("m_youku") else youku_headers
            html_a_list, page_html = self.youku_crawl.crawl_youku_list(base_url, s_word, headers, page)
        else:
            return make_response(jsonify({'code': -1, 'message': 'not have search type.'}), 400)
        # if not base_url:
        #     return False

        return {"code": 100, "message": "SUCCESS", "data": html_a_list, "page_html": page_html} if \
            html_a_list or page_html else {"code": -100, "message": "fail get search page."}

    @api.expect(SearchModel.post_form_request())
    @api.doc(params={"action": "方法"})
    def post(self):
        return jsonify({'message': 'successful crawl news.'})
