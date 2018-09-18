# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from .settings import IMAGES_STORE


class DownImg(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = str(item['image_url'])
        yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['item']['image_url'].split('/')[-1]
        return image_name


class TiebaPipeline(object):

    def open_spider(self, spider):
        print(spider)
        self.file = open('tieba.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        print(spider)
        item['image_location'] = IMAGES_STORE + item['image_url'].split('/')[-1]
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + '\n', )
        return item

    def close_spider(self, spider):
        print(spider)
        self.file.close()
