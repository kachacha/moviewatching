# -*- coding:UTF-8 -*-
from flask import Flask, request
from flask import jsonify
from flask import render_template

import get_mo_list

app = Flask(__name__)


@app.route('/jh')
def hello_world():
    return jsonify(msg="111")


@app.route('/runningpage/<m_id_n>')
def runningpage(m_id_n):
    print(987978897, m_id_n)
    word = str(m_id_n).rsplit('&&&')[0]
    m_id_n = str(m_id_n).rsplit('&&&')[1]
    get_m_list = get_mo_list.get_aiqiyi_list(word)
    print(get_m_list)
    sear_data = {}
    for one in get_m_list['m_date_list']:
        if one['m_name'] == m_id_n:
            sear_data = one
        else:
            continue
    if sear_data == {}:
        return render_template("error.html")
    else:
        api = 'http://www.sfsft.com/video.php?url='
        url = sear_data['m_href'].split('#')[0]
        print(url)
        target = api + url
        context = {
            'title': m_id_n,
            'target': target
        }
        return render_template("runningpage.html", **context)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template("list_page.html")
    elif request.method == 'POST':
        print(request.form['formname'], request.form['formid'])
        get_m_list = get_mo_list.get_aiqiyi_list(request.form['formname'])
        # print(get_m_list)
        context = {
            'm_name': request.form['formname'],
            'get_m_list': get_m_list['m_date_list']
        }
        return render_template("list_page.html", **context)


if __name__ == '__main__':
    app.run('0.0.0.0', port=2435)

# class video_downloader():
#     def __init__(self, url):
#         self.server = 'http://api.xfsub.com'
#         self.api = 'http://api.xfsub.com/xfsub_api/?url='
#         self.get_url_api = 'http://api.xfsub.com/xfsub_api/url.php'
#         self.url = url.split('#')[0]
#         self.headers = {'Referer': 'http://api.xfsub.com/xfsub_api/?url=%s?qqdrsign=055a4' % self.url}
#         self.target = self.api + self.url
#         self.s = requests.session()
#
#     """
# 	函数说明:获取key、time、url等参数
# 	Parameters:
# 		无
# 	Returns:
# 		无
# 	Modify:
# 		2017-09-18
# 	"""
#
#     def get_key(self):
#         print(self.target)
#         req = self.s.get(url=self.target)
#         req.encoding = 'utf-8'
#         self.info = json.loads(re.findall('"url.php",\ (.+),', req.text)[0])  # 使用正则表达式匹配结果，将匹配的结果存入info变量中
#
#     """
# 	函数说明:获取视频地址
# 	Parameters:
# 		无
# 	Returns:
# 		video_url - 视频存放地址
# 	Modify:
# 		2017-09-18
# 	"""
#
#     def get_url(self):
#         data = {'time': self.info['time'],
#                 'key': self.info['key'],
#                 'url': self.info['url'],
#                 'type': ''}
#         req = self.s.post(url=self.get_url_api, data=data, headers=self.headers)
#         url = self.server + json.loads(req.text)['url']
#         req = self.s.get(url=url, headers=self.headers)
#         bf = BeautifulSoup(req.text, 'xml')  # 因为文件是xml格式的，所以要进行xml解析。
#         video_url = bf.find('file').string  # 匹配到视频地址
#         return video_url
#
#     """
# 	函数说明:回调函数，打印下载进度
# 	Parameters:
# 		a b c - 返回信息
# 	Returns:
# 		无
# 	Modify:
# 		2017-09-18
# 	"""
#
#     def Schedule(self, a, b, c):
#         per = 100.0 * a * b / c
#         if per > 100:
#             per = 1
#         sys.stdout.write("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')
#         sys.stdout.flush()
#
#     """
# 	函数说明:视频下载
# 	Parameters:
# 		url - 视频地址
# 		filename - 视频名字
# 	Returns:
# 		无
# 	Modify:
# 		2017-09-18
# 	"""
#
#     def video_download(self, url, filename):
#         request.urlretrieve(url=url, filename=filename, reporthook=self.Schedule)
#
#
# if __name__ == '__main__':
#     url = 'http://www.iqiyi.com/v_19rr7qhfg0.html#vfrm=19-9-0-1'
#     vd = video_downloader(url)
#     filename = '加勒比海盗5'
#     print('%s下载中:' % filename)
#     vd.get_key()
#     video_url = vd.get_url()
#     print('  获取地址成功:%s' % video_url)
#     vd.video_download(video_url, filename + '.mp4')
#     print('\n下载完成！')
