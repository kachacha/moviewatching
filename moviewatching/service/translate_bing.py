__author__ = "张峰"
__copyright__ = "© 2016-2018 中云开源技术（上海）有限公司保留一切权利。"
__version__ = "v1.0"
__maintainer__ = "zhangf"
__email__ = "zhangf@zylliondata.com"
__status__ = "Development"
__date__ = "2019-09-23"

from .request_untils import ToolsUntils


class TranslateBing:
    def __init__(self):
        """
        Bing 国内版 翻译 爬虫
        """
        self.tools_untils = ToolsUntils()
        self.bing_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://cn.bing.com',
            'referer': 'https://cn.bing.com/translator/',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.132 Safari/537.36',

        }

    def get_bing_re_data(self, keyword: str, to_l: str, from_l='auto') -> dict:
        """

        :param keyword: 关键词
        :param to_l: 需要翻译的语言  auto:auto-detect
        :param from_l: 原语言
        to : en（英语）
        to : ja（日语）

        :return: return translate result data.
        """

        bing_uri = "https://cn.bing.com/ttranslatev3?isVertical=1&&IG=0C8441CC05E14F89960E40AFF9E5A727&IID=translator.5028.1"
        querydata = {
            "text": keyword,
            "to": "zh-Hans" if to_l.__eq__("zh") else to_l
        }
        if from_l == "auto":
            querydata["fromLang"] = "auto-detect"
        get_json_data = self.tools_untils.open_post_url(bing_uri, querydata, self.bing_headers)
        print("Bing", get_json_data)
        try:
            re__json = {
                "code": 100,
                'message': 'success',
                'sourceWord': keyword,
                'sourceLanguage': get_json_data[0]['detectedLanguage']['language'],
                'translationWord': get_json_data[0]['translations'][0]['text'],
                'translationLanguage': get_json_data[0]['translations'][0]['to'],
                'other': get_json_data[0],
                'translationSource': 'Bing'
            }
        except:
            re__json = {'code': -100, 'message': 'fails'}
        return re__json
