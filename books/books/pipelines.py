# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import xlsxwriter


class BooksPipeline(object):
    def open_spider(self, spider):
        spider.row = 1
        spider.col = 0
        # 新建Excel文件
        # spider.workbook = xlsxwriter.Workbook('./dangdang_book.xlsx')
        spider.workbook = xlsxwriter.Workbook('./dangdang_all_book.xlsx')
        # 新建工作表
        spider.worksheet = spider.workbook.add_worksheet()
        # 工作表首行内容
        spider.worksheet.write('A1', '一级分类')
        spider.worksheet.write('B1', '二级分类')
        spider.worksheet.write('C1', '作者')
        spider.worksheet.write('D1', '书名')
        spider.worksheet.write('E1', '价格')
        spider.worksheet.write('F1', '简介')
        # spider.worksheet.write('G1', '当当链接')
        # spider.worksheet.write('H1', '分类代号')

    def close_spider(self, spider):
        # 关闭文件
        spider.workbook.close()

    def process_item(self, item, spider):
        # 从第一行开始写入
        spider.worksheet.write_string(spider.row, spider.col, item['first_cate'])
        spider.worksheet.write_string(spider.row, spider.col + 1, item['second_cate'])
        spider.worksheet.write_string(spider.row, spider.col + 2, item['book_author'])
        spider.worksheet.write_string(spider.row, spider.col + 3, item['book_title'])
        spider.worksheet.write_string(spider.row, spider.col + 4, str(item['book_price']))
        # 去除简介中的'\u3000'
        item['book_descs'] = re.sub('\u3000', '', item['book_descs'])
        spider.worksheet.write_string(spider.row, spider.col + 5, item['book_descs'])
        # spider.worksheet.write_string(spider.row, spider.col + 6, item['book_url'])
        # spider.worksheet.write_string(spider.row, spider.col + 7, item['data_type'])
        # print(item)

        # 行数+1 列数归0
        spider.row += 1
        spider.col = 0
        return item
