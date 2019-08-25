# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os, uuid
from scrapy.exporters import JsonItemExporter


class EcommerceCategoriesPipeline(object):
    def process_item(self, item, spider):
        return item


class EcommerceListingItemsPipeline(object):
    def __init__(self, spider_name):
        self.export_dir = spider_name
        self.item_list_filename = "items.json"
        # will be instantiated in `open_spider` function
        self.file_pointer = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider.name)

    def open_spider(self, spider):
        # ensure directory named  `spider_name` exists
        if not os.path.isdir(self.export_dir):
            os.mkdir(self.export_dir)
        self.file_pointer = open(os.path.join(self.export_dir, self.item_list_filename), 'wb')
        self.exporter = JsonItemExporter(self.file_pointer, indent=0)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_pointer.close()

    def process_item(self, item, spider):
        html_filename = self._get_new_filename(self.export_dir, '.html')
        with open(html_filename, 'wb') as fout:
            fout.write(item.pop('response_body'))
        item['file_name'] = html_filename
        self.exporter.export_item(item)
        return item

    @staticmethod
    def _get_new_filename(dir, extension=''):
        extension = '.' + extension if not extension.startswith('.') else extension
        file_name = None
        while file_name is None:
            random_str = uuid.uuid4().hex
            random_filename = os.path.join(dir, random_str + extension)
            if not os.path.exists(random_filename):
                file_name = random_filename
                break
        return file_name
