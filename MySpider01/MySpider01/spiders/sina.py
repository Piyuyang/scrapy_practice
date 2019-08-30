# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com']
    start_urls = ['https://news.sina.cn']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="swiper-wrapper"]/li')
        for li in li_list:
            item = dict()
            item['title'] = li.xpath('./a/h2/em/text()').extract_first()
            item['url'] = li.xpath('./a/@href').extract_first()
            yield item
