# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

client = MongoClient("mongodb+srv://chiluser:chilchilbl@cluster0.bh9pd.mongodb.net/")
db = client.chilchil
goods_col = db.chil_items

class ChilchilCrawlPipeline(object):
    # collection_name = 'chil_items'

    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    # def open_spider(self, spider):
    #     self.client = MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        author_dict = None
        if (item['author'] != None):
            author_dict = {
                'author': item['author'],
                'author_id': item['author_id']
            }
        # elif (item['writer'] and item['drawer']):
        #     author_dict = {
        #         'drawer': {
        #             'author': item['drawer'],
        #             'author_id': item['drawer_id']
        #         },
        #         'writer': {
        #             'author': item['writer'],
        #             'author_id': item['writer_id']
        #         }
        #     }
        # category_dict = {
        #         'category': item['category'],
        #         'category_id': item['category_id']
        #     }
        publisher_dict = {
                'publisher': item['publisher'],
                'publisher_id': item['publisher_id']
            } if item['publisher'] else None
        label_dict = {
                'label': item['label'],
                'label_id': item['label_id']
            } if item['label'] else None
         # seme tags
         # uke tags
         # erodo
         # play
         # settei
         # tone
         

        goods_item = {
            'goods_id': item['goods_id'],
            'title': item['title'], 
            'author': author_dict,
            # 'category': category_dict,
            'publisher': publisher_dict,
            'label': label_dict,
            'sales_date': item['sales_date'],
            'price': item['price'],
            'isbn': item['isbn'],
            'seme': item['seme'],
            'uke': item['uke'],
            'erodo': item['erodo'],
            'settei': item['settei'],
            'tone': item['tone']
        }

        goods_col.insert_one(goods_item)
        return item
