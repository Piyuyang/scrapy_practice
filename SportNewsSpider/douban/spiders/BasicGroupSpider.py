# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import DoubanItem
import re
from scrapy.selector import Selector

import urllib2
import string
import json


class GroupSpider(CrawlSpider):
    name = "Group"  # 爬虫名
    allowed_domains = ["sports.sina.com.cn"]  # 允许爬虫的域名
    start_urls = [
        "http://sports.sina.com.cn/",  # 爬虫初始请求地址
    ]
    """
    rules: 是Rule对象的集合，用于匹配目标网站并排除干扰
    参数有
    link_extractor：连接筛选器（allow：满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配）
    callback：回调请求函数
    follow：默认是false，爬取和start_url符合的url。
            如果是True的话，就是爬取页面内容所有的以start_urls开头的url。
    process_links：要进行处理的链接
    process_request：要进行的处理请求
    """
    rules = [
        Rule(SgmlLinkExtractor(allow=('[0-9]\.shtml$',)), callback='parse_group_home_page',
             process_request='add_cookie'),
        Rule(SgmlLinkExtractor(allow=('/$',)), follow=True, process_request='add_cookie'),
    ]

    def add_cookie(self, request):
        request.replace(cookies=[
            {'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': 'sports.sina.com.cn', 'path': '/'},
        ])
        return request

    def parse_group_topic_list(self, response):
        pass

    def parse_group_home_page(self, response):  # 处理地址对应的响应
        hxs = HtmlXPathSelector(response)
        item = DoubanItem()

        sel = Selector(response)

        item['Html'] = sel.xpath("//html").extract()  # extract()--》序列化该节点为unicode字符串并返回list。
        # get Source
        item['Source'] = 'sina'
        # get URL
        item['URL'] = response.url
        # get ID
        try:
            newsid = sel.xpath("//head/meta[@name='comment']/@content").extract()
            strid = "".join(newsid)
            item['ID'] = strid[3:]
        except:
            item['ID'] = '-1'
        # get Time
        try:
            time = sel.xpath("id('pub_date')/text()").extract()
            item['Time'] = time[0]
        except:
            item['Time'] = '-1'
        # get keywords
        try:
            words = sel.xpath("//head/meta[@name='tags']/@content").extract()
            item['Keyword'] = ",".join(words)
        except:
            item['Keyword'] = '-1'
        # get Comment  找到返回json数据的url
        try:
            str1 = 'http://comment5.news.sina.com.cn/page/info?format=json&channel=ty&newsid='
            str2 = '&group=0&compress=1&ie=gbk&oe=gbk&page=1&page_size=100&jsvar=requestId_24959748'
            url = str1 + item['ID'] + str2
            page = urllib2.urlopen(url).read()
            jsonVal = json.loads(page.decode("gbk"))
        except:
            jsonVal = '-1'
            print "comment url error!"
        item['Comment'] = jsonVal
        # get hotness
        try:
            item['Reply'] = str(jsonVal["result"]["count"]["qreply"])
            item['Total'] = str(jsonVal["result"]["count"]["total"])
            item['Show'] = str(jsonVal["result"]["count"]["show"])
        except:
            item['Reply'] = '-1'
            item['Total'] = '-1'
            item['Show'] = '-1'
        # get Title
        try:
            title = sel.xpath("id('artibodyTitle')/text()").extract()
            item['Title'] = title[0]
        except:
            title = sel.xpath("//title/text()").extract()
            item['Title'] = title[0]
            artical = sel.xpath("/html/body//p").extract()
            item['Artical'] = "".join(artical)
            return item
        # get artical
        artical = sel.xpath("id('artibody')//p/text()").extract()
        item['Artical'] = "".join(artical)

        return item
