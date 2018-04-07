# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from .items import IndexItem, DetailItem
from scrapy.contrib.exporter import CsvItemExporter

'''
class IndexJsonPipeline(object):
    def __init__(self):
        self.file = open('/home/kiri/tmp/index.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item: IndexItem, spider):
        if isinstance(item, IndexItem):
            self.exporter.export_item(item)
            return item


class DetailJsonPipeline(object):
    def __init__(self):
        self.file = open('/home/kiri/tmp/detail.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item: DetailItem, spider):
        if isinstance(item, DetailItem):
            self.exporter.export_item(item)
            return item
'''

'''
class JsonPipeline(object):
    def __init__(self):
        self.file1 = open('index.json', 'wb')
        self.file2 = open('detail.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter1 = JsonItemExporter(self.file1, encoding='utf-8', ensure_ascii=False)
        self.exporter2 = JsonItemExporter(self.file2, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()

    def close_spider(self, spider):
        self.exporter1.finish_exporting()
        self.file1.close()
        self.exporter2.finish_exporting()
        self.file2.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        if isinstance(item, IndexItem):
            self.exporter1.export_item(item)
            return item
        else:
            self.exporter2.export_item(item)
            return item
'''


class CSVPipeline(object):
    '''
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        from scrapy import signals
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file1 = open('index.csv', 'w+b')
        self.exporter1 = CsvItemExporter(self.file1)
        self.exporter1.start_exporting()
        self.file2 = open('detail.csv', 'w+b')
        self.exporter2 = CsvItemExporter(self.file1)
        self.exporter2.start_exporting()
    '''

    def __init__(self):
        self.file1 = open('index.csv', 'wb')
        self.file2 = open('detail.csv', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter1 = CsvItemExporter(self.file1, encoding='gbk')
        self.exporter2 = CsvItemExporter(self.file2, encoding='gbk')
        # 开启倒数
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()

    def spider_closed(self, spider):
        self.exporter1.finish_exporting()
        self.file1.close()
        self.exporter2.finish_exporting()
        self.file2.close()

    def process_item(self, item, spider):
        if isinstance(item, IndexItem):
            self.exporter1.export_item(item)
            return item
        else:
            self.exporter2.export_item(item)
            return item
