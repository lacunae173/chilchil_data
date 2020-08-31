# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class ChilUpdatePipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'test')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.column = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # review_count = scrapy.Field()
    # vote_count = scrapy.Field()
    # kami_percent = scrapy.Field()
    # score = scrapy.Field()
    # average_vote = scrapy.Field()
    # vote_items_count = scrapy.Field()
        update = {
            'vote_count' : item['vote_count'],
            'kami_percent' : item['kami_percent'],
            'score' : item['score'],
            'average_vote' : item['average_vote'],
            'vote_items_count' : item['vote_items_count']
        }
        self.column.update_one({
            'goods_id': item['goods_id']
        }, {
            '$set': update
        }, upsert=False)
        return item

class UpdateAuthorFieldPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'test')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.column = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        author = item['author'] if item['author'] else {'writer': item['writer'], 'drawer': item['drawer']}
        itemdb = self.column.find_one({'goods_id': item['goods_id'], 'author': {'$type': "object"}, "author.writer":None})
        if itemdb:
            self.column.update_one({
            'goods_id': item['goods_id']
            }, {
                '$set': {
                    'author': author
                }
            }, upsert=False)
        return item

class ChilchilCrawlPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'test')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.column = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        author = item['author'] if item['author'] else {'writer': item['writer'], 'drawer': item['drawer']}
        goods_item = {
            'goods_id': item['goods_id'],
            'title': item['title'], 
            'author': author,
            'publisher': item['publisher'],
            'label': item['label'],
            'sales_date': item['sales_date'],
            'price': item['price'],
            'isbn': item['isbn'],
            'seme': item['seme'],
            'uke': item['uke'],
            'erodo': item['erodo'],
            'play': item['play'],
            'settei': item['settei'],
            'tone': item['tone'],
            'vote_count' : item['vote_count'],
            'kami_percent' : item['kami_percent'],
            'score' : item['score'],
            'average_vote' : item['average_vote'],
            'vote_items_count' : item['vote_items_count']
        }
        # if not self.column.find_one({'goods_id': item['goods_id']}):
        self.column.insert_one(goods_item)
        return item
