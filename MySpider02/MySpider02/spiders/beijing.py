# -*- coding: utf-8 -*-
import scrapy

from MySpider02.items import Myspider02Item


class BeijingSpider(scrapy.Spider):
    """北京市人民政府-要闻动态-工作动态"""
    name = 'beijing'  # 爬虫名称
    allowed_domains = ['beijing.gov.cn']  # 允许爬虫的域名
    start_urls = ['http://www.beijing.gov.cn/ywdt/gzdt/']  # 爬虫开始的url
    page = 1

    def parse(self, response):
        """处理列表页"""
        # 分组，所需数据都在li标签下
        li_list = response.xpath('//div[@class="listBox"]//li')
        for li in li_list:
            item = Myspider02Item()  # 实例化item
            item['title'] = li.xpath('./a/text()').extract_first()  # 标题
            href = li.xpath('./a/@href').extract_first()  # 链接

            item['href'] = self.start_urls[0] + href[2:]

            yield scrapy.Request(
                item['href'],  # 请求地址
                callback=self.parse_detail,  # 请求成功后执行的函数
                meta={"item": item}  # 向函数传递的数据
            )

        # 翻页，构造下一页地址
        next_url = 'http://www.beijing.gov.cn/ywdt/gzdt/default_%d.htm' % self.page
        # 发起请求
        yield scrapy.Request(
            next_url,
            callback=self.parse,
        )
        self.page += 1

    def parse_detail(self, response):
        """处理详情页"""
        item = response.meta.get('item')  # 获取由meta传递来到item
        span = response.xpath('//div[@id="othermessage"]/p/span/text()').extract()
        item['pub_time'] = span[0][3:]  # 发布时间
        item['source'] = span[1][3:]  # 信息来源
        # 正文内容被分段放在p标签中
        p_list = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
        content = '\n'.join(p_list)
        item['content'] = content
        yield item
