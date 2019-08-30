# -*- coding: utf-8 -*-
import json
from urllib import request

import scrapy

from books import settings


class AllDangdangSpider(scrapy.Spider):
    name = 'all_dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://e.dangdang.com/list-WY1-dd_sale-0-1.html']
    next_url = 'http://e.dangdang.com/media/api.go?' \
               'action=mediaCategoryLeaf&promotionType=1&deviceSerialNo=html5&macAddr=html5' \
               '&channelType=html5&permanentId=20190819204207688204722703073553861&returnType=json&channelId=70000' \
               '&clientVersionNo=5.8.4&platformSource=DDDS-P&fromPlatform=106&deviceType=pconline&token=' \
               '&start=%d&end=%d&category=%s&dimension=dd_sale&order=0'

    def parse(self, response):
        # 获取一级分类、二级分类、分类代号对应关系
        category_dict = dict()  # 二级分类:一级分类
        code_name_dict = dict()  # 二级分类:代号

        # 大分类
        li_list = response.xpath('//ul[@class="second_level"]/li')
        for li in li_list:
            # 小分类
            a_list = li.xpath('./ul/a')
            for a in a_list:
                first_cate = li.xpath('./a/h4/text()').extract_first()
                second_cate = a.xpath('./li/text()').extract_first()
                data_type = a.xpath('./li/@data-type').extract_first()
                category_dict[second_cate] = first_cate
                code_name_dict[second_cate] = data_type

                # 构建请求地址，获取该分类下的图书总数
                start = 0
                end = 20
                next_url = self.next_url % (start, end, data_type)
                with request.urlopen(next_url) as f:
                    json_data = json.loads(f.read().decode('utf-8'))
                total = json_data['data']['total']

                while start <= 20:
                    next_url = self.next_url % (start, end, data_type)
                    start += 21
                    end += 21

                    req = request.Request(next_url)
                    req.add_header('User-Agent', settings.USER_AGENT)
                    # 请求网页
                    with request.urlopen(req) as f:
                        json_data = json.loads(f.read().decode('utf-8'))
                    # 获取数据
                    data = json_data['data']
                    book_list = data.get('saleList', [])
                    for book in book_list:
                        item = dict()
                        item['first_cate'] = category_dict[second_cate]
                        item['second_cate'] = second_cate
                        # 获取图书信息
                        book_detail = book['mediaList'][0]
                        item['book_title'] = book_detail.get('title', '')
                        item['book_author'] = book_detail.get('authorPenname', '')
                        item['book_descs'] = book_detail.get('descs', '')
                        item['book_price'] = book_detail.get('salePrice', '')
                        yield item
