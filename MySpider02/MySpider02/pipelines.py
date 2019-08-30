# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class Myspider02Pipeline(object):
    def process_item(self, item, spider):
        item['content'] = self.process_content(item['content'])
        print(item)
        return item

    def process_content(self, content):
        # 去除正文中的'\u3000'
        content = re.sub('\u3000', '', content)
        return content
