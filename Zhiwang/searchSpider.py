# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import random
import re


def get_result(ybcode, page=1):  # 数据的请求
    data = {'ybcode': ybcode, 'entrycode': '', 'page': page, 'pagerow': '20'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url = "http://data.cnki.net/Yearbook/PartialGetCatalogResult"
    params = urllib.parse.urlencode(data).encode(encoding='utf-8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    res = str(r.read(), 'utf-8')
    return res


def get_pageno(ybcode):  # 获取总页数
    soup = BeautifulSoup(get_result(ybcode), 'lxml')
    pages = int(soup.select('.s_p_listl')[0].get_text().split("共")[2].split('页')[0])
    print('总共' + str(pages) + '页')
    return pages


def dataclear(data):  # 数据的清理，除去文本中所有的\n和\r
    data = re.sub('\n+', ' ', data)
    data = re.sub('\r+', ' ', data)
    data = re.sub(' +', ' ', data)
    return data


def filedata(ybcode):  # 下载知网的统计年鉴之类的所有excel表
    pageno = get_pageno(ybcode)
    for i in range(1, pageno + 1, 1):
        print('########################################当前第' + str(i) + '页###################################')
        soup = BeautifulSoup(get_result(ybcode, i), 'lxml')
        for j in soup.select('tr'):
            s = BeautifulSoup(str(j), 'lxml')
            if len(s.select('img[src="/resources/design/images/nS_down2.png"]')) == 0:
                pass
            else:
                try:
                    if len(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a')) >= 2:
                        title = str(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(1) > a')[0].get_text())
                        url = 'http://data.cnki.net' + BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a')[
                            1].get('href')
                        title = dataclear(title)  # 若不清洗数据，则文件名中会包含\n等特殊字符，导致文件下载错误
                        filedown(title, url)
                        print(title)
                except Exception as e:
                    print('error:-------------------' + str(e))
                    pass


def filedown(title, url):  # 文件下载函数
    try:
        r = requests.get(url)
        with open(title + ".xls", "wb") as code:
            code.write(r.content)
    except Exception as e:
        pass
    x = random.randint(1, 2)
    time.sleep(x)


if __name__ == '__main__':
    ybcode = 'N2013060059'  # 更改此项可下载其他年鉴
    filedata(ybcode)
