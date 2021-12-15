__author__ = "张峰"
__copyright__ = "© 2016-2018 中云开源技术（上海）有限公司保留一切权利。"
__version__ = "v1.0"
__maintainer__ = "zhangf"
__email__ = "zhangf@zylliondata.com"
__status__ = "Development"
__date__ = "2019-09-23"

from enum import Enum, unique

from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields

from ..service.translate_baidu import TranslateBaidu
from ..service.translate_bing import TranslateBing

api = Namespace('translate api', description='爬爬翻译接口')


@unique
class Action(Enum):
    DAG = 'dag'
    TASK = 'task'


class Params(fields.Raw):
    def format(self, value):
        return {"params": {}}


class BuilderModel(Params):

    #  # 链接构造
    @staticmethod
    def get_request():
        get_parser = api.parser()
        get_parser.add_argument('keyword', type=str, help='输入关键词', required=True, default='')
        get_parser.add_argument('from', type=str, help='原语言', required=False, default='auto')
        get_parser.add_argument('to', type=str, help='翻译成语言', required=True, default='en')
        get_parser.add_argument('source', type=str, help='选择来源', required=False, default='auto')
        return get_parser

    @staticmethod
    def post_form_request():
        parser = api.parser()
        return parser


@api.route('/translate')
class builderApi(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.translateBing = TranslateBing()
        self.translateBaidu = TranslateBaidu()

    @api.expect(BuilderModel.get_request())
    def get(self):
        keyword = request.args.get('keyword', "", str)
        from_language = request.args.get('from', "auto", str)  # zh/auto
        to_language = request.args.get('to', "en", str)
        source = request.args.get('source', "auto", str)
        # bing_judge = request.args.get("bing_", True, bool)
        bool_to_re = 0
        __json = {
            "code": 100,
            'message': 'success',
            'sourceWord': keyword,
            'sourceLanguage': '',
            'translationWord': '',
            'translationLanguage': '',
            'other': '',
            'translationSource': ''
        }
        if source == "Bing":
            __json = self.translateBing.get_bing_re_data(keyword, to_language, from_language)
            bool_to_re = __json.get('code')
        elif source == "Baidu":
            __json = self.translateBaidu.translate(keyword, to_language, from_language)
            bool_to_re = __json.get('code')
        else:
            if bool_to_re <= 0:
                __json = self.translateBing.get_bing_re_data(keyword, to_language, from_language)
                bool_to_re = __json.get('code')
            if bool_to_re <= 0:
                __json = self.translateBaidu.translate(keyword, to_language, from_language)
                bool_to_re = __json.get('code')
            if bool_to_re > 0:
                return make_response(jsonify(__json), 200)
            else:
                return make_response(jsonify({'code': -1, 'message': 'fails'}), 400)
        if bool_to_re > 0:
            return make_response(jsonify(__json), 200)
        else:
            return make_response(jsonify({'code': -1, 'message': 'fails'}), 400)

    # @api.expect(BuilderModel.get_request())
    # def get(self):
    #     keyword = request.args.get('keyword', "", str)
    #     from_language = request.args.get('from', "auto", str)  # zh/auto
    #     to_language = request.args.get('to', "en", str)
    #     bing_judge = request.args.get("bing_", True, bool)
    #     baidu_judge = request.args.get("baidu_", False, bool)
    #     youdao_judge = request.args.get("youdao_", False, bool)
    #     re_data = {}
    #     if bing_judge:
    #         re_data["bing__json"] = self.translateBing.get_bing_re_data(keyword, to_language, from_language)
    #     if baidu_judge:
    #         re_data["baidu__json"] = self.translateBaidu.translate(keyword, to_language, from_language)
    #     if youdao_judge:
    #         re_data["youdao__json"] = {}
    #
    #     return jsonify({'message': 'successful crawl news.', 'get_translate_data': re_data})

    @api.expect(BuilderModel.post_form_request())
    @api.doc(params={"action": "方法"})
    def post(self):
        return jsonify({'message': 'successful crawl news.'})
