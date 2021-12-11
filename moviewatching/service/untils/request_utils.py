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
import urllib
from http.cookiejar import CookieJar
# import urllib.request
from urllib import request

import chardet
import requests


# headers = {
#     # 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
#     # Chrome/58.0.3029.110 Safari/537.36"}
#     'Cookie': "__jsluid=4d044fb26a4b60f17bc3eddc4e918488; "
#               "UM_distinctid=15e9e65676622f-0b589ff77a3214-36624308-1fa400-15e9e656767c7b; tlb_cookie1=114ui_8280; "
#               "tlb_cookie=43query_8080; CNZZDATA1261033118=271122604-1505892342-null%7C1508570664; "
#               "Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1508563610; "
#               "Hm_lpvt_cdb4bc83287f8c1282df45ed61c4eac9=1508575563; JSESSIONID=1C7A5E494C25B984D14D2ED03F2E7417-n1:1",
#     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/61.0.3163.100 Safari/537.36"}


class RequestsUtils:
    def __init__(self):
        """
        翻译所需各种组件
        """

    @staticmethod
    def requests_t(url, aiqiyi_headers):
        res = requests.get(url, headers=aiqiyi_headers)
        if res.status_code == 200 or res.status_code == 201:
            return res.text
        else:
            return False

    @staticmethod
    def open_get_header(url: str, headers: dict) -> dict or str:
        res = urllib.request.urlopen(url).read()
        mychar = chardet.detect(res)
        # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        print(mychar)
        bianma = mychar['encoding']  # 获得网页编码（如utf-8）
        # print(bianma)
        res = urllib.request.Request(url, headers=headers)
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        response = opener.open(res)
        raw_response = response.read().decode(bianma, errors='ignore')
        print(raw_response)
        return raw_response

    @staticmethod
    def urlopen_url(url: str) -> dict or str:
        res = urllib.request.urlopen(url).read()
        mychar = chardet.detect(res)
        if res.status_code > 201:
            return None
        # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        print(mychar)
        bianma = mychar['encoding']  # 获得网页编码（如utf-8）
        # print(bianma)
        res = urllib.request.Request(url)
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        response = opener.open(res)
        raw_response = response.read().decode(bianma, errors='ignore')
        return raw_response

    @staticmethod
    def open_get_header1(url: str, headers: dict) -> dict or str:
        res = urllib.request.Request(url, None, headers=headers)  # f发送一个requet请求
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))  # 防反爬
        response = opener.open(res)
        print(response.read())
        mychar = chardet.detect(response.read())
        print(mychar)
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
