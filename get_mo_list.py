import urllib.request

import requests
from bs4 import BeautifulSoup

aiqiyi_headers = {
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'so.iqiyi.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}


def requests_t(url):
    res = requests.get(url, headers=aiqiyi_headers)
    print(res.text)
    print(res.status_code)
    if res.status_code == 200:
        return res.text
    else:
        return False


def get_url(typec, mname=None):
    # return False if not typec else print("come requests .")
    p_data_mname = urllib.request.quote(mname)
    # print(p_data_mname)
    baseUrl = 'https://so.iqiyi.com/so/q_' + p_data_mname + '?source=history&refersource=lib&sr=741573544309'
    get_data = requests_t(baseUrl)
    if get_data:
        return BeautifulSoup(get_data, 'html5lib')
    else:
        return False


def get_tengxun_list(mname):
    # url https://v.qq.com/x/search/?q=%E6%88%98%E7%8B%BC&stag=0&smartbox_ab=
    print()

def get_aiqiyi_list(mname):
    get_date = get_url(typec="aiqiyi", mname=mname)
    if not get_date:
        return {'m_date_list': []}
    try:
        ul_list = get_date.find('ul', class_='mod_result_list')
        li_list = ul_list.find_all('li', class_='list_item')
    except:
        return {'m_date_list': []}
    m_date_list = []
    for One_li in li_list:
        m_date = {}
        try:
            m_info_item_bottom = One_li.find('div', class_='info_item_bottom')
            testsss = str(m_info_item_bottom.text)
            if '爱奇艺' in str(testsss) and '立即播放' in testsss:
                a_href = m_info_item_bottom.find('a')['href']
                print(a_href)
                m_date['m_href'] = a_href
            else:
                continue
        except Exception as e:
            continue
        m_name = One_li.find('h3', class_='result_title').find('a')['title']
        # print(m_name)
        m_date['m_name'] = m_name
        m_director_list = []
        m_director_info_item = One_li.find_all('div', class_='info_item')
        m_director = m_director_info_item[0].find_all('div', class_='result_info_cont')
        for one_m_director in m_director:
            m_director_list.append(str(one_m_director.text).replace(' ', '').replace('\n', ''))
        # print(m_director_list)
        m_date['m_director_list'] = m_director_list
        m_contest = str(m_director_info_item[1].text).replace(' ', '').replace('\n', '')
        # print(m_contest)
        m_date['m_contest'] = m_contest
        m_date_list.append(m_date)
    return {'m_date_list': m_date_list}


if __name__ == '__main__':
    print(get_aiqiyi_list('加勒比海盗'))
