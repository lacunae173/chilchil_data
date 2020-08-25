# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChilchilCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    goods_id = scrapy.Field()
    title = scrapy.Field()
    # 著者
    author = scrapy.Field()
    author_id = scrapy.Field()
    # # 作画
    # drawer = scrapy.Field()
    # drawer_id = scrapy.Field()
    # # 原作
    # writer = scrapy.Field()
    # writer_id = scrapy.Field()
    # # 媒体
    # category = scrapy.Field()
    # category_id = scrapy.Field()
    # 出版社
    publisher = scrapy.Field()
    publisher_id = scrapy.Field()
    # レーベル
    label = scrapy.Field()
    label_id = scrapy.Field()
    # 発売日
    sales_date = scrapy.Field()
    # 価格
    price = scrapy.Field()
    isbn = scrapy.Field()
    # seme tags
    seme = scrapy.Field()
    # uke tags
    uke = scrapy.Field()
    # erodo
    erodo = scrapy.Field()
    # play
    #play = scrapy.Field()
    # settei
    settei = scrapy.Field()
    # tone
    tone = scrapy.Field()