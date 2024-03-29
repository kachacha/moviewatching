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

# 爱奇艺视频相关配置
iqiyi_base_search_url = "https://so.iqiyi.com/so/q_{0}_ctg__t_0_p_1_qc_0_rd__site_iqiyi_m_1_bitrate__af_0"  # 第一页
iqiyi_more_search_url = "https://so.iqiyi.com/so/q_{0}_ctg__t_0_page_{1}_p_1_qc_0_rd__site_iqiyi_m_1_bitrate__af_0"  # 第n页
iqiyi_headers = {
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'so.iqiyi.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}
iqiyi_m_search = "https://m.iqiyi.com/search.html?key={0}"
iqiyi_m_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'sec-ch-ua-platform': 'Android',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'
}

# 腾讯视频相关配置
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
qq_m_search = "https://m.v.qq.com/search.html?keyWord={0}"
qq_m_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    'sec-ch-ua-platform': 'Android',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'
}

# 优酷视频相关配置
youku_base_search_url = "https://so.youku.com/search_video/q_{0}"
youku_more_search_url = "https://so.youku.com/search_video/q_{0}"
youku_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br", "accept-language": "zh-CN,zh;q=0.9,en;q=0.8", "cache-control": "max-age=0",
    "cookie": "ctoken=maGkN_lSo_gGxm8kp31HhJMo; __ysuid=1637049872853Hax; __ayft=1637049872854; UM_distinctid=17d27c6bce5893-01f6f7e443f322-57b1a33-1fa400-17d27c6bce6ce7; cna=qERDGtvjSXgCATohoLO6NQ3F; _m_h5_tk=a0a7447ed62ff81464a7dbd6dd994591_1640173213856; _m_h5_tk_enc=f9c92cb3bb14a8e7f73684631d67474c; __aysid=1640168516214IMn; __ayscnt=4; modalFrequency={\"UUID\":\"10\"}; P_ck_ctl=E893CE9E46EC813838D265375D8EA08B; xlly_s=1; __arycid=dd-3-00; __arcms=dd-3-00; __ayvstp=15; __aysvstp=2; youku_history_word=%5B%22%25E6%2588%2591%25E4%25BB%25AC%25E6%2581%258B%25E7%2588%25B1%25E5%2590%25A7%22%2C%22%25E6%2580%25AA%25E4%25BE%25A0%25E4%25B8%2580%25E5%2589%25AA%25E6%25A2%2585%22%2C%22%25E4%25B8%2580%25E5%2589%25AA%25E6%25A2%2585%22%2C%22%25E4%25B8%258D%25E6%2583%2591%25E4%25B9%258B%25E6%2597%2585%22%2C%22%25E8%259C%2598%25E8%259B%259B%25E4%25BE%25A0%22%5D; __arpvid=1640168793383aLUtva-1640168793395; __aypstp=47; __ayspstp=6; isg=BE5OFSIxo3upWReBecG93c3fnyQQzxLJ0WUFTXiXltEM2-814F0Z2BqJFQe3WArh; l=eBE9MFungpvjDQFBBOfanurza77OSIRYYuPzaNbMiOCPOQfB53uFW6dq-LY6C3GVh6uyR35T8LLDBeYBq3xonxvTr9mT2uHmn; tfstk=cMuFBgA3yeLeFR4WDyayAChiotcdwBhnZNPbxD-ervjtzWfmZTFgdWFaN1Wux",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
    "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
youku_m_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    'sec-ch-ua-platform': 'Android',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'
}
