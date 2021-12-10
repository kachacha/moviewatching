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
import sys
import urllib.request

from moviewatching.service.untils.request_utils import RequestsUtils


class Crawl:

    def __init__(self):
        self.request_util = RequestsUtils()
        """
        爬取解析相关
        """

    def crawl_iqiyi_list(self, base_url: str, s_word: str, headers: dict, page=1) -> str:
        p_s_word = urllib.request.quote(s_word if s_word else "")
        get_html_res = self.request_util.open_get_header(base_url.format(p_s_word, page), headers=headers)
        # print(get_html_data)
        if not get_html_res:
            return ""
        try:
            layout_main = get_html_res.find('div', class_='layout-main')
            layout_main.find("div", class_='search-container-filter').decompose()
            layout_main.find("div", class_='qy-search-top-tips').decompose()
        except Exception as e:
            logging.warning(
                "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
            return ""
        print(layout_main)
        return layout_main


if __name__ == '__main__':
    print()
    # print(Crawl().crawl_iqiyi_list('加勒比海盗'))
