# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Myspider01Pipeline(object):
    def process_item(self, item, spider):
        with open('sina.txt', 'a') as f:
            f.write(str(item))
            f.write('\n')
        return item
