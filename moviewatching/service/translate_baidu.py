__author__ = "张峰"
__copyright__ = "© 2016-2018 中云开源技术（上海）有限公司保留一切权利。"
__version__ = "v1.0"
__maintainer__ = "zhangf"
__email__ = "zhangf@zylliondata.com"
__status__ = "Development"
__date__ = "2019-09-24"

import json
import re

import execjs
import requests


class TranslateBaidu:

    def __init__(self):
        self._query = ""
        self.TOKEN = "843ec4f4336aa1c580ad0f0856ec9978"
        self.COOKIE = "BAIDUID=71F3248EB11A403AB67FA7A2E7B184FD:FG=1"
        self.GET_URL = 'https://fanyi.baidu.com/?aldtype=16047'
        self.POST_URL = 'https://fanyi.baidu.com/v2transapi'
        self.LAN_POST_URI = "https://fanyi.baidu.com/langdetect"  # 百度检测语言

        self.GET_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.baidu.com',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.POST_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Accept': '*/*',
            'cookie': self.COOKIE,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.baidu.com',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
            'X-Requested-With': 'XMLHttpRequest',
            'content-length': '1000'
        }

        self._session = requests.session()
        self._data = {
            'from': 'zh',
            'to': 'en',
            'transtype': 'realtime',
            'simple_means_flag': '3',
            # 'query': '',  # 要翻译的词或句, 变项
            # 'sign': '',  # Ajax(js) 加密, 变项
            # 'token': '819a3d27d7719966c56deaf30f3f4162',  # 不变项
        }
        # 可以直接拿浏览器上的 token, 因为 token 是不变的
        self._get_token()

    def _get_token(self):
        response = self._session.get(self.GET_URL, headers=self.GET_HEADERS)
        html = response.text
        li = re.search(r"<script>\s*window\[\'common\'\] = ([\s\S]*?)</script>", html)
        token = re.search(r"token: \'([a-zA-Z0-9]+)\',", li.group(1))
        # self.GET_HEADERS['cookie'] = "locale=zh; BAIDUID=" + BAIDUID
        self._data['token'] = self.TOKEN

    def _get_langdetect(self, query: str):
        """
        todo 获取输入词的语言
        :param query:
        :return:
        """
        _data = {
            'query': query
        }
        response = self._session.post(self.LAN_POST_URI, data=_data, headers=self.POST_HEADERS)
        dict_data = json.loads(response.content.decode())
        if dict_data["error"] < 0 or 'success'.find(dict_data['msg']) < 0:
            self._data['from'] = 'zh'
        else:
            self._data['from'] = dict_data['lan']

    def _get_sign(self):
        # 将 使用 js 加密的函数 copy 到 baidu_translate.js 文件中
        # 然后使用 execjs 执行
        with open('moviewatching/service/untils/baidu_translate.js') as fp:
            sign = execjs.compile(fp.read()).call('e', self._query)
            self._data['sign'] = sign

    def _ready(self, from_l: str):
        self._get_sign()
        if from_l.find('auto') >= 0:
            self._get_langdetect(self._query)
        else:
            self._data['from'] = from_l

    def translate(self, query: str, to_l: str, from_l='auto') -> dict:
        self._data['query'] = self._query = query
        self._data['to'] = to_l
        self._ready(from_l)
        response = self._session.post(self.POST_URL, data=self._data, headers=self.POST_HEADERS)
        dict_data = json.loads(response.content.decode())
        print(dict_data)
        if dict_data.get("error", None):
            re__json = {'code': -100, 'message': 'fails'}
            return re__json
        else:
            re__json = {
                "code": 100,
                'message': 'success',
                'sourceWord': query,
                'sourceLanguage': self._data['from'],
                'translationWord': dict_data['trans_result']['data'][0]['dst'],
                'translationLanguage': dict_data['trans_result']['to'],
                'other': dict_data,
                'translationSource': 'Baidu'
            }
            return re__json


if __name__ == "__main__":
    trans = TranslateBaidu()
    print(trans.translate('ぎじゅつ', "en", "zh"))
