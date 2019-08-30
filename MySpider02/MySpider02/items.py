# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Myspider02Item(scrapy.Item):
    title = scrapy.Field()  # 标题
    href = scrapy.Field()  # 链接
    source = scrapy.Field()  # 来源
    pub_time = scrapy.Field()  # 发布时间
    content = scrapy.Field()  # 正文内容
