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
from lxml import etree
from selenium import webdriver

query = '刘亦菲'
'''下载图片'''


def download1(src, pic_id):
    dir_name = './刘亦菲1/' + str(pic_id) + '.jpg'
    try:
        pic = requests.get(src, timeout=10)
        fp = open(dir_name, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


def get_json_data():
    for i in range(0, 25, 20):
        '''for 循环请求全部的url'''
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
            download1(image['src'], image['id'])


def download2(src, pic_id):
    dir_name = './刘亦菲2/' + str(pic_id) + '.webp'
    # 因为从xpath获取到的url的海报图片格式是.webp,所以如果变成.jpg是打不开文件的
    try:
        pic = requests.get(src, timeout=10)
        fp = open(dir_name, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


def get_pic_xpath():
    # 使用XPath自动下载刘亦菲的海报封面
    for i in range(0, 30, 15):
        # 循环作用是模拟翻页，最简单的方式是翻到底，很少有人能有150个作品
        driver = webdriver.Chrome()
        request_url = 'https://search.douban.com/movie/subject_search?search_text=' \
                      + query + '&cat=1002&start=' + str(i)
        driver.get(request_url)
        html = etree.HTML(driver.page_source)
        # selenium 的 page_source 可以直接返回页面源码
        # 参考：https://blog.csdn.net/MTbaby/article/details/77573443
        # etree.HTML():构造了一个XPath解析对象并对HTML文本进行自动修正。
        """
        XPath定位特定位置的几种基础表达方式
        xpath(‘node’) 选取了 node 节点的所有子节点；
        xpath(’/div’) 从根节点上选取 div 节点；
        xpath(’//div’) 选取所有的 div 节点；
        xpath(’./div’) 选取当前节点下的 div 节点；
        xpath(’…’) 回到上一个节点；xpath(’//@id’) 选取所有的 id 属性；
        xpath(’//book[@id]’) 选取所有拥有名为 id 的属性的 book 元素；
        xpath(’//book[@id=“abc”]’) 选取所有 book 元素，且这些 book 元素拥有 id= "abc"的属性；
        xpath(’//book/title | //book/price’) 选取 book 元素的所有 title 和 price 元素。
        """
        src_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
        title_xpath = "//div[@class='item-root']/div[@class='detail']" \
                      "/div[@class='title']/a[@class='title-text']"
        # XPath Helper 使用时Win10系统安装好后，ctrl+shift+z调出界面
        # 之后按Shift然后鼠标可以选中元素，就会出现相应的XPath元素

        srcs = html.xpath(src_xpath)
        titles = html.xpath(title_xpath)
        for src, title in zip(srcs, titles):
            download2(src, title.text)


get_json_data()
get_pic_xpath()  # 得到的结果里有一些并没有刘亦菲的作品
