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

import json
import logging
import os
import re
import sys
from urllib.parse import quote, urlparse, parse_qs

from bs4 import BeautifulSoup
from flask import current_app

from ..untils.pymongo_util import PyMongoUtil
from ..untils.request_utils import RequestsUtils


class Crawl:

    def __init__(self):
        self.request_util = RequestsUtils()
        self.obtain_utils = ObtainUtils()

        self.episode_collection = PyMongoUtil(
            uri=current_app.config.get("MONGODB_URI"),
            db=current_app.config.get("MONGODB_DB"),
            collection=current_app.config.get("MONGODB_TABLE_VIDEO_INFO")
        )
        """
        爬取解析相关
        """

    def crawl_qq_list(self, base_url: str, s_word: str, headers: dict, page=1) -> tuple:
        p_s_word = quote(s_word if s_word else "")
        # get_html_res = self.request_util.requests_t(base_url.format(p_s_word, page), headers)
        # if not get_html_res:
        get_html_res = self.request_util.urlopen_set_chardet_url(base_url.format(p_s_word, page), "UTF-8")
        if not get_html_res:
            return [], ""
        try:
            get_html_res = BeautifulSoup(get_html_res, 'html5lib')
            search_container = get_html_res.find('div', id='search_container')
            layout_main = get_html_res.find('div', class_='wrapper_main')
            try:
                layout_main.find("div", class_='mod_filter_box').decompose()  # 去除头
                layout_main.find("div", class_='result_relative').decompose()  # 去除关键词搜索
                layout_main.find("div", class_='mod_pages').decompose()  # 去除页数
                layout_main.find("a", class_='desc_more').decompose()  # 去除杂项
                layout_main.find("a", class_='tip_download __lite_hide__').decompose()  # 去除杂项
            except Exception as e:
                logging.warning(
                    "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
                pass
            a_list = layout_main.findAll("a")
            movie_list = []
            set_href_list = []
            pattern = re.compile(u'https://v.qq.com/x/[^\s]*.html[^\s]*')
            for _a in a_list:
                href_url = pattern.search(str(_a.get("href")))
                if href_url and href_url[0] not in set_href_list:
                    set_href_list.append(href_url[0])
                    one_href = href_url[0].replace('"', "")
                    movie_list.append({"uri": '"' + one_href + '"',
                                       "html": str(_a).replace(one_href,
                                                               '"' + "javascript:toPlayMessage('" + one_href + "')" + '"')})

            to_href_url = pattern.findall(search_container.__str__())
            # todo 替换全局 target="_blank" 为空 否则点击跳转到另一个页面不播放了
            search_container = search_container.__str__().replace('target="_blank"', '')
            set_href_list2 = []
            for one_href in to_href_url:
                one_href = one_href.replace('"', "")
                if one_href not in set_href_list2:
                    set_href_list2.append(one_href)
                    search_container = search_container.__str__().replace('"' + one_href + '"',
                                                                          '"' + "javascript:toPlayMessage('" + one_href + "')" + '"')
        except Exception as e:
            logging.warning(
                "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
            return [], ""
        # print(movie_list)
        return movie_list, search_container.__str__()

    def crawl_m_qq_list(self, base_url: str, s_word: str, headers: dict) -> tuple:
        p_s_word = quote(s_word if s_word else "")
        # get_html_res = self.request_util.requests_t(base_url.format(p_s_word, page), headers)
        # if not get_html_res:
        get_html_res = self.request_util.urlopen_set_chardet_url(base_url.format(p_s_word), "UTF-8")
        if not get_html_res:
            return [], ""
        try:
            get_html_res = BeautifulSoup(get_html_res, 'html5lib')
            result = get_html_res.find('div', id='result')
            try:
                result.find("div", class_='mod_filter_box').decompose()  # 去除头
                result.find("div", class_='result_relative').decompose()  # 去除关键词搜索
                result.find("div", class_='mod_pages').decompose()  # 去除页数
                result.find("a", class_='desc_more').decompose()  # 去除杂项
                result.find("a", class_='tip_download __lite_hide__').decompose()  # 去除杂项
            except Exception as e:
                logging.warning(
                    "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
                pass
            a_list = result.findAll("a")
            movie_list = []
            set_href_list = []
            pattern = re.compile(u'http[s]{0,1}://m.v.qq.com/cover/[^\s]*/[^\s]*.html[^\s]*')
            for _a in a_list:
                href_url = pattern.search(str(_a.get("href")))
                if href_url and href_url[0] not in set_href_list:
                    set_href_list.append(href_url[0])
                    one_href = href_url[0].replace('"', "")
                    movie_list.append({"uri": '"' + one_href + '"',
                                       "html": str(_a).replace('"' + one_href + '"',
                                                               '"' + "javascript:toPlayMessage('" + one_href + "')" + '"')})

            to_href_url = pattern.findall(result.__str__())
            # todo 替换全局 target="_blank" 为空
            result = result.__str__().replace('target="_blank"', '')
            set_href_list2 = []
            for one_href in to_href_url:
                one_href = one_href.replace('"', "")
                if one_href not in set_href_list2:
                    set_href_list2.append(one_href)
                    # print(one_href)
                    result = result.__str__().replace('"' + one_href + '"',
                                                      '"' + "javascript:toPlayMessage('" + one_href + "')" + '"')
        except Exception as e:
            logging.warning(
                "{} -- {} - {}: {}".format(os.path.basename(__file__), __file__, sys._getframe().f_lineno, str(e)))
            return [], ""
        # print(movie_list)
        return movie_list, result.__str__()

    def crawl_episode(self, page_uri: str, headers: dict) -> dict:
        "http://m.v.qq.com/cover/m/m441e3rjq9kwpsc.html?vid=h00415t94pe"  # 腾讯手机版uri
        "https://v.qq.com/x/cover/m441e3rjq9kwpsc/b0041fx801u.html"  # 腾讯电脑版uri
        if page_uri.__contains__("m.v.qq.com"):
            page_id, episode_id = self.obtain_utils.get_page_id_and_episode_id(page_uri)
            page_uri = "https://v.qq.com/x/cover/" + page_id + "/" + episode_id + ".html"
        elif page_uri.__contains__("v.qq.com"):
            pass
        else:
            return {}
        get_html_res = self.request_util.urlopen_set_chardet_url(page_uri, "UTF-8")
        if not get_html_res:
            return {}
        get_cover_info = self.obtain_utils.get_COVER_INFO(get_html_res)
        if not get_cover_info:
            return get_cover_info
        get_cover_info["s_type"] = "qq"
        # todo
        # self.episode_collection.insert_one(**get_cover_info)
        re_res_data_list = []
        video_id = get_cover_info.get("id", "")
        for index, one_cover in enumerate(get_cover_info.get("nomal_ids", [])):
            re_res_data = {}
            if one_cover.get("F", 0) == 4:
                re_res_data["cover"] = "notice"
            else:
                re_res_data["cover"] = "positive"
            re_res_data["label"] = "第" + (index + 1).__str__() + "集"
            re_res_data["video_url"] = "https://v.qq.com/x/cover/" + video_id + "/" + one_cover.get("V", "") + ".html"
            re_res_data_list.append(re_res_data)
        return {"video_list": re_res_data_list}


class ObtainUtils:

    def __init__(self):
        """
        各个解析拆分回去值或内容方法
        """

    @staticmethod
    def get_page_id_and_episode_id(page_uri) -> tuple:
        result = urlparse(page_uri)
        page_id = result.path.__str__().split("/")[-1].replace(".html", "")
        query = parse_qs(result.query)
        episode_id = query.get('vid', [""])[0]
        return page_id, episode_id

    @staticmethod
    def get_COVER_INFO(html_res: str) -> dict:
        get_cover_info = re.findall("var COVER_INFO = (.*?)var", html_res, re.S)
        try:
            get_cover_info_json = json.loads(get_cover_info[0])
            if "id" not in get_cover_info_json.keys():
                return {}
        except IndexError as e:
            return {}
            # raise IndexError({"code": -101, "message": "获取集数失败！" + e.__str__()})
        return get_cover_info_json


if __name__ == '__main__':
    print(ObtainUtils().crawl_episode("http://m.v.qq.com/cover/m/m441e3rjq9kwpsc.html?vid=h00415t94pe"))
    # 爱奇艺视频相关配置
    qq_base_search_url = "https://v.qq.com/x/search/?q={0}"  # 第一页
    qq_more_search_url = "https://v.qq.com/x/search/?q={0}&cur={1}"  # 第n页
    qq_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        # "cookie":"iip=0; tvfe_boss_uuid=b1a5aa241634055d; pgv_pvid=9431298544; _ga=GA1.2.1211606922.1612418484; verifysession=h014824aa580ce867d5b12a9f332a633ac2afbc4a641a8f186913fccd022020c5be9c74f203983ef1cf; RK=kY6NKPo7Zw; ptcz=7f6ed0f14d4eb821052f0200319379f2539f90a542539c2e4c916f70a8d30621; qqmusic_uin=; qqmusic_key=; qqmusic_fromtag=; pgv_info=ssid=s2389460765&pgvReferrer=; rv2=808D0F85A280F4E9B0D0E551A5F7027E6E84407050F923C821; property20=A77C9D13395F3EF0C1A0F45897A32CFB0D1C9EAC2B10DA759C264766752367975D8881D38F0DA773; _qpsvr_localtk=0.6976694070642708; o_cookie=752561131; vversion_name=8.2.95; pac_uid=1_752561131; video_platform=2; video_guid=b3d72b6a9dc07b7a; video_omgid=b3d72b6a9dc07b7a; ts_refer=www.baidu.com/link; ts_uid=3492555168; bucket_id=9231005; tvfe_search_uid=b3b45ee4-2944-4b70-85b4-8817c66fa41c; txv_boss_uuid=409350de-e8f4-8dfc-011b-621fa9d3fe59; qv_als=IULIoVDF6iSzl7OHA11637117623VusjhQ==; pvpqqcomrouteLine=newsdetail; tokenParams=%3FG_Biz%3D18%26tid%3D336626; eas_sid=Z1T6l3s7q241x7L0v4U9Z611G0; ts_last=v.qq.com/x/search/; ptag=www_baidu_com; ad_play_index=61",
        "if-modified-since": "Fri, 10 Dec 2021 11:00:00 GMT",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\",\"Chromium\";v=\"96\",\"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # print(Crawl().crawl_qq_list(qq_base_search_url, '速度与激情', qq_headers))
