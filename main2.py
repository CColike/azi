# -*- coding: utf-8 -*-
import json
import os
import re
import shutil
import ssl
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from random import choice
from lxml import etree

#设置请求头等参数，防止被反爬
headers = {
   'Accept': '*/*',
   'Accept-Language': 'en-US,en;q=0.5',
   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
}
def get_user_agent():
   '''获取随机用户代理'''
   user_agents = [
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
       "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
       "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
       "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
       "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
       "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
       "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
       "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
       "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
       "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
       "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
       "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
       "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
       "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
       "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
       "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
       "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
       "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
       "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",
       "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
       "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）"
   ]
   # 在user_agent列表中随机产生一个代理，作为模拟的浏览器
   user_agent = choice(user_agents)
   return user_agent

def re_video_info(text, pattern):
    '''利用正则表达式匹配出视频信息并转化成json'''
    match = re.search(pattern, text)
    # print(match.group(1))
    if (pattern=='"videoData":(.*?),"upData":{'):
        print(match.group(1))

    return json.loads(match.group(1))

def video_selector(aid):
    origin_video_url = 'https://www.bilibili.com/video/' + aid
    headers.update({'User-Agent':get_user_agent()})
    res = requests.get(origin_video_url, headers=headers)
    # print(res.text)
    html = etree.HTML(res.text)#res.text 实际上是F12中的“网络”->“响应”的一个文本文件
    try:
        video_num = int(html.xpath('/html/body/div[2]/div[4]/div[2]/div/div[5]/div[1]/div[1]/span/text()')[0].split('/')[1][:-1])
        #video_num = int(re_video_info(res.text, '"videoData":(.*?),"upData":{').split('/')[1][:-1])
        # <span class="cur-page">(1/58)</span>
        # etree.html是将爬取的网页数据再生成标准网页格式数据，因为有些网页不规范写的时候
        # etree.parse是对标准网页格式数据进行解析用的
        video_info_temp = re_video_info(res.text, '"videoData":(.*?),"upData":{')
        #这样直接在字符串中进行匹配，然后将他转化成json，如果转化报错，去https://www.bejson.com/explore/index_new/看一眼
        #在线html、json格式化工具
        video_arr=[(aid+'/?p='+str(i+1),video_info_temp["pages"][i]["part"])for i in range(video_num)]

        return video_arr
    except:
        return [(aid, html.xpath('// *[ @ id = "viewbox_report"] / h1/text()')[0]), ]

def video_download(aid,acc_quality,begin_idx):
    p_list=video_selector(aid)
    for i in range(begin_idx-1,len(p_list)):
        print(p_list[i][0])
        single_download(p_list[i],acc_quality)
        time.sleep(10)######

def single_download(aid, acc_quality):
    '''单个视频实现下载'''
    # 请求视频链接，获取信息
    origin_video_url = 'https://www.bilibili.com/video/' + aid[0]
    res = requests.get(origin_video_url, headers=headers)
    title=aid[1]
    print('您当前正在下载：', title)

    video_info_temp = re_video_info(res.text, '__playinfo__=(.*?)</script><script>')
    video_info = {}
    # 获取视频质量
    quality = video_info_temp['data']['accept_description'][acc_quality]
    # 获取视频时长
    video_info['duration'] = video_info_temp['data']['dash']['duration']
    # 获取音频链接
    audio_url = video_info_temp['data']['dash']['audio'][acc_quality]['baseUrl']
    # 计算视频时长
    video_time = int(video_info.get('duration', 0))
    video_minute = video_time // 60
    video_second = video_time % 60
    print('当前视频清晰度为{}，时长{}分{}秒'.format(quality, video_minute, video_second))
    # 调用函数下载保存视频
    download_video_single(origin_video_url, audio_url, title)

def download_video_single(referer_url, audio_url, title):
    """单个视频下载"""
    # 更新请求头
    headers.update({"Referer": referer_url})
    print("音频下载开始：%s" % title)
    # 下载并保存音频
    audio_content = requests.get(audio_url, headers=headers)
    print('%s\t音频大小：'%title, round(int(audio_content.headers.get('content-length',0))/1024/1024,2),'\tMB')
    received_audio = 0
    with open('%s.mp3' % title, 'ab') as output:
        headers['Range'] = 'bytes=' + str(received_audio) + '-'
        response = requests.get(audio_url, headers=headers)
        output.write(response.content)
        received_audio += len(response.content)
    print("音频下载结束：%s" % title)

# single_download("BV1wr4y1v7TA",0)
# video_download("BV1wr4y1v7TA",0)
# video_download("BV1gq4y167mq",0,174)
# video_download("BV1Ya411z7WL",0,35)
# BV1tS4y1C7Rk
# BV19P4y1P75w
video_download("BV1bi4y1f7fy",0,1)