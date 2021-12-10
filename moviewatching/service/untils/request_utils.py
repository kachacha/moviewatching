#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "crawl.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/10"
__time__ = "17:58:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

import json
from urllib import request

import chardet
import requests
from aiohttp import CookieJar


class RequestsUtils:
    def __init__(self):
        """
        翻译所需各种组件
        """

    @staticmethod
    def requests_t(url, aiqiyi_headers):
        res = requests.get(url, headers=aiqiyi_headers)
        print(res.status_code)
        if res.status_code == 200 or res.status_code == 201:
            return res.text
        else:
            return False

    @staticmethod
    def open_get_header(url: str, headers: dict) -> dict or str:
        res = request.Request(url, None, headers=headers)  # f发送一个requet请求
        cj = CookieJar()  # 防反爬
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        response = opener.open(res)
        mychar = chardet.detect(response.read())
        # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        bianma = mychar['encoding']  # 获得网页编码（如utf-8）
        raw_response = response.read().decode(bianma, errors='ignore')
        return raw_response

    @staticmethod
    def open_get_url(url: str) -> dict or str:
        res = request.Request(url, None)  # f发送一个requet请求
        cj = CookieJar()  # 防反爬
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        response = opener.open(res)
        mychar = chardet.detect(response.read())
        # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        bianma = mychar['encoding']  # 获得网页编码（如utf-8）
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
        try:
            get_re_data = json.loads(response.text)
        except Exception as e:
            get_re_data = str(e) + ": " + response.text
        return get_re_data
