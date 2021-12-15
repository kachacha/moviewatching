#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "crawl.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/9"
__time__ = "17:58:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

import logging
import os
import re
import sys
from urllib.parse import quote

from bs4 import BeautifulSoup

from moviewatching.service.untils.request_utils import RequestsUtils


class Crawl:

    def __init__(self):
        self.request_util = RequestsUtils()
        """
        爬取解析相关
        """

    def crawl_iqiyi_list(self, base_url: str, s_word: str, headers: dict, page=1) -> tuple:
        p_s_word = quote(s_word if s_word else "")
        get_html_res = self.request_util.requests_t(base_url.format(p_s_word, page), headers)
        if not get_html_res:
            get_html_res = self.request_util.urlopen_url(base_url.format(p_s_word, page))
            if not get_html_res:
                return [], ""
        try:
            get_html_res = BeautifulSoup(get_html_res, 'html5lib')
            layout_main = get_html_res.find('div', class_='layout-main')
            layout_main.find("div", class_='search-container-filter').decompose()
            layout_main.find("div", class_='qy-search-top-tips').decompose()
            a_list = layout_main.findAll("a")
            movie_list = []
            set_href_list = []
            for _a in a_list:
                pattern = re.compile(u'www.iqiyi.com/v_[^\s]*.html')
                href_url = pattern.search(str(_a))
                if href_url and href_url[0] not in set_href_list:
                    set_href_list.append(href_url[0])
                    movie_list.append({"uri": href_url[0],
                                       "html": str(_a).replace("//" + href_url[0],
                                                               "./play?play_uri=" + href_url[0])})
        except Exception as e:
            logging.warning(
                "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
            return [], ""
        # print(movie_list)
        return movie_list, ""

    def crawl_m_iqiyi_list(self, base_url: str, s_word: str, headers: dict) -> tuple:
        p_s_word = quote(s_word if s_word else "")
        get_html_res = self.request_util.requests_t(base_url.format(p_s_word), headers)
        if not get_html_res:
            get_html_res = self.request_util.urlopen_url(base_url.format(p_s_word))
            if not get_html_res:
                return "", ""
        try:
            get_html_res = BeautifulSoup(get_html_res, 'html5lib')
            div_app_id = get_html_res.find("div", id="app")
            # print(div_app_id)
        except Exception as e:
            logging.warning(
                "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
            return "", ""
        # print(movie_list)
        return "", div_app_id.__str__()


if __name__ == '__main__':
    # 爱奇艺视频相关配置
    aiqiyi_base_search_url = "https://so.iqiyi.com/so/q_{0}?source=history&refersource=lib&sr=741573544309"  # 第一页
    aiqiyi_more_search_url = "https://so.iqiyi.com/so/q_{0}_ctg__t_0_page_{1}_p_1_qc_0_rd__site_iqiyi_m_1_bitrate__af_0"  # 第n页
    aiqiyi_headers = {
        'Host': 'so.iqiyi.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    print(Crawl().crawl_iqiyi_list(aiqiyi_base_search_url, '加勒比海盗', aiqiyi_headers))
