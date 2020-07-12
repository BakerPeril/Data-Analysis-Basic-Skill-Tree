#!/usr/bin/env python
# encoding: utf-8
"""
@author: BakerPeril
@contact: bakerperil@163.com
@software: python3.7
@time: 2020-07-11 18:51
"""
# 本例代码来自 陈旸-数据分析实战45讲-Python爬虫：如何自动化下载王祖贤海报
# 使用XPath自动下载刘亦菲的海报
# 之前版本可以有一些小改动
# 1、对于如果没有预先创建'./刘亦菲2/'的文件夹是不是程序可以自己做
# 2、搜索所得到的数据会有不存在刘的影视作品，这里做一个判断，如果没有刘，这可以不下载该文件
import requests
import json
import os
from lxml import etree
from selenium import webdriver

query = '刘亦菲'
'''下载图片'''

pic_path = 'F:\\DA_Algorithm_Python\\Apriori\\刘亦菲picture'
if not os.path.isdir(pic_path):
    # 做一步判断是否存在所想要存储的路径，存在的话就继续进行
    # 不存在的话，则创建一个路径来进行存储
    os.mkdir(pic_path)


def download2(src, pic_id):
    dir_name = pic_path + '\\' + str(pic_id) + '.webp'
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
        src_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
        title_xpath = "//div[@class='item-root']/div[@class='detail']" \
                      "/div[@class='title']/a[@class='title-text']"
        name_xpath = "//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']"
        # XPath Helper 使用时Win10系统安装好后，ctrl+shift+z调出界面
        # 之后按Shift然后鼠标可以选中元素，就会出现相应的XPath元素

        srcs = html.xpath(src_xpath)
        titles = html.xpath(title_xpath)
        name_lists = html.xpath(name_xpath)

        for src, title, name_list in zip(srcs, titles, name_lists):
            if name_list.text is None:  # 做一步判断演员名字列表中是否存在刘亦菲的名字
                continue
            names = name_list.text.replace(' ', '').split('/')
            # 打印出的演员带有空格，因此如果不加去掉空格无法执行下载函数
            print(names)
            if query in names:
                download2(src, title.text)


get_pic_xpath()

