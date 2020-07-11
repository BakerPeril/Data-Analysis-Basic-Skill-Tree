#!/usr/bin/env python
# encoding: utf-8
"""
@author: BakerPeril
@contact: bakerperil@163.com
@software: python3.7
@time: 2020-07-11 18:51
"""
# 本例代码来自 陈旸-数据分析实战45讲-Python爬虫：如何自动化下载王祖贤海报

# 使用JSON数据自动下载刘亦菲的海报
import requests
import json

query = '刘亦菲'
'''下载图片'''


def download(src, pic_id):
    dir_name = './刘亦菲/' + str(pic_id) + '.jpg'
    try:
        pic = requests.get(src, timeout=10)
        fp = open(dir_name, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


'''for 循环请求全部的url'''
for i in range(0, 25, 20):
    # 另外为了减少运行时间，就暂时设定为25，实际图片数量13616{..."total":13616,"limit":20,"more":true}
    url = 'https://www.douban.com/j/search_photo?q=' + query + '&limit=20&start=' + str(i)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.181 Safari/537.36'
    }
    # 添加headers，是因为豆瓣网站及aloe反爬机制，对于不加headers会导致服务器判定其为爬虫，因此随意加了一个headers
    html = requests.get(url, headers=headers).text  # 得到返回的结果

    response = json.loads(html, encoding='utf-8')  # 将JOSN格式转换成Python对象
    print(response)
    for image in response['images']:
        print(image['src'])
        download(image['src'], image['id'])

# 使用XPath自动下载刘亦菲的海报封面
