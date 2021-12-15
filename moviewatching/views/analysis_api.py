#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "analysis_api.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/13"
__time__ = "17:45:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

from enum import Enum, unique

from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields

from ..config import iqiyi_base_search_url, iqiyi_more_search_url, qq_base_search_url, qq_more_search_url, \
    iqiyi_headers, qq_headers
from ..service.analysis_uri import AnalysisUri

api = Namespace('Analysis Api', description='vip解析链接管理接口')


@unique
class Action(Enum):
    DAG = 'dag'
    TASK = 'task'


class Params(fields.Raw):
    def format(self, value):
        return {"params": {}}


class AnalysisModel(Params):

    #  # 链接构造
    @staticmethod
    def get_random_one():
        get_parser = api.parser()
        # get_parser.add_argument('s_type', type=str, help='搜索平台', required=True, default='')
        # get_parser.add_argument('s_word', type=str, help='搜索关键词', required=False, default='auto')
        # get_parser.add_argument('page', type=int, help='页数', required=True, default=1)
        return get_parser

    @staticmethod
    def post_form_request():
        parser = api.parser()
        return parser


@api.route('/analysis')
class AnalysisApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.analysis_uri = AnalysisUri()

    @api.expect(AnalysisModel.get_random_one())
    def get(self):
        s_type = request.args.get('s_type', "qq", str)
        s_word = request.args.get('s_word', "", str)
        page = request.args.get('page', 1, int)
        if s_type.__eq__("iqiyi"):
            base_url = iqiyi_more_search_url if page > 1 else iqiyi_base_search_url
            headers = iqiyi_headers
            iqiyi_list = self.iqiyi_crawl.crawl_iqiyi_list(base_url, s_word, headers, page)
        elif s_type.__eq__("qq"):
            base_url = qq_more_search_url if page > 1 else qq_base_search_url
            headers = qq_headers
            iqiyi_list = self.qq_crawl.crawl_qq_list(base_url, s_word, headers, page)
        else:
            return make_response(jsonify({'code': -1, 'message': 'not have search type.'}), 400)
        # if not base_url:
        #     return False

        return {"code": 100, "message": "SUCCESS", "data": iqiyi_list} if \
            iqiyi_list else {"code": -100, "message": "fail get search page."}

    @api.expect(AnalysisModel.post_form_request())
    @api.doc(params={"action": "方法"})
    def post(self):
        return jsonify({'message': 'successful crawl news.'})


@api.route('/analysis-plus')
class AnalysisPlusApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.analysis_uri = AnalysisUri()

    @api.expect(AnalysisModel.get_random_one())
    def get(self):
        get_analysis = self.analysis_uri.get_random_one()
        return {"code": 100, "message": "SUCCESS", "data": get_analysis} if \
            get_analysis else {"code": -100, "message": "fail get random analysis uri."}
