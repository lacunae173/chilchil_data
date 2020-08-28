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
    def process_item(self, item, spider):
        goods_item = {
            'goods_id': item['goods_id'],
            'title': item['title'], 
            'author': item['author'],
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
            'tone': item['tone']
        }
        goods_col.insert_one(goods_item)
        return item
