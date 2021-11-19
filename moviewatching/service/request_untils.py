__author__ = "张峰"
__copyright__ = "© 2016-2018 中云开源技术（上海）有限公司保留一切权利。"
__version__ = "v1.0"
__maintainer__ = "zhangf"
__email__ = "zhangf@zylliondata.com"
__status__ = "Development"
__date__ = "2019-09-23"

import json
from urllib import request

import chardet
import requests
from aiohttp import CookieJar


class ToolsUntils:
    def __init__(self):
        """
        翻译所需各种组件
        """

    @staticmethod
    def open_get_url(url: str) -> dict or str:
        res = request.Request(url, None)  # f发送一个requet请求
        cj = CookieJar()  # 防反爬
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        response = opener.open(res)
        mychar = chardet.detect(response.read())
        # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        bianma = mychar['encoding']  # 获得网页编码（如utf-8）
        # res = request.Request(url, None)
        # cj = CookieJar()
        # opener = request.build_opener(request.HTTPCookieProcessor(cj))
        # response = opener.open(res)
        raw_response = response.read().decode(bianma, errors='ignore')
        return raw_response

    @staticmethod
    def open_post_url(url: str, querydata: dict, headers: dict) -> dict or str:
        """

        :param url:
        :param querydata:
        :param headers:
        :return:
        """
        # 空的对象，body参数
        response = requests.post(url=url, data=querydata, headers=headers)
        # print(response.text)
        try:
            get_re_data = json.loads(response.text)
        except Exception as e:
            get_re_data = response.text
        return get_re_data
