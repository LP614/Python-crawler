# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy
import pymongo
from pymongo import MongoClient
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# 下载图片
class ToutaioImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1] + '.jpg'
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image DownloadedFailed')
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            yield Request(image_url)


# mongodb
class ToutiaoTwoMongoPipeline():
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        问题：数据存入数据库之后，出现大量重复数据
        解决思路：
        在process_item中执行数据插入之前，先对变量进行复制copy，再用复制copy的变量进行操作，通过互斥确保变量不被修改。因此，修正这个问题，我们只需要调整优化下process_item()方法。
        解决代码：process_item()     - copy.deepcopy(item)   ->导入copy包
        """
        asynItem = copy.deepcopy(item)
        infos = {'chinese_tag': asynItem['chinese_tag'], 'title': asynItem['title'], 'source': asynItem['source'],
                 'image_url': asynItem['image_url']}
        self.db.toutiao.insert(infos)
        return item
