# -*- coding: utf-8 -*-
import json

import scrapy


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://e.dangdang.com/list-WY1-dd_sale-0-1.html']

    def parse(self, response):
        # 大分类分组，如：小说、青春文学、文学、动漫二次元
        li_list = response.xpath('//ul[@class="second_level"]/li')
        for li in li_list:
            # item = dict()
            # item['first_cate'] = li.xpath('./a/h4/text()').extract_first()
            # item['first_url'] = li.xpath('./a/@href').extract_first()
            # 小分类
            a_list = li.xpath('./ul/a')
            for a in a_list:
                item = dict()
                item['first_cate'] = li.xpath('./a/h4/text()').extract_first()
                item['second_cate'] = a.xpath('./li/text()').extract_first()
                item['data_type'] = a.xpath('./li/@data-type').extract_first()
                item['second_url'] = a.xpath('./@href').extract_first()
                if item['second_url'] is not None:
                    yield scrapy.Request(
                        url=item['second_url'],
                        callback=self.parse_book_list,
                        meta={'item': item}
                    )

    def parse_book_list(self, response):
        # 获取传递过来的item
        item = response.meta.get('item')
        a_list = response.xpath('//div[@id="book_list"]/a')
        for a in a_list:
            item['book_url'] = a.xpath('./@href').extract_first()
            item['book_title'] = a.xpath('./div[@class="bookinfo"]/div[1]/text()').extract_first()
            item['book_author'] = a.xpath('./div[@class="bookinfo"]/div[2]/text()').extract_first()
            item['book_price'] = a.xpath('./div[@class="bookinfo"]/div[4]/span/text()').extract_first()[1:]
            item['book_descs'] = a.xpath('./div[@class="bookinfo"]/div[5]/text()').extract_first()
            if item['book_descs'] is None:
                item['book_descs'] = ''
            yield item
