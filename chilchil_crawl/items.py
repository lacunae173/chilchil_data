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
    # 原作
    writer = scrapy.Field()
    # 作画
    drawer = scrapy.Field()
    # 出版社
    publisher = scrapy.Field()
    # レーベル
    label = scrapy.Field()
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
    play = scrapy.Field()
    # settei
    settei = scrapy.Field()
    # tone
    tone = scrapy.Field()
    # review_count
    review_count = scrapy.Field()
    # vote_count
    vote_count = scrapy.Field()
    # percent of 5 votes
    kami_percent = scrapy.Field()
    # score calculated by chilchil
    score = scrapy.Field()
    average_vote = scrapy.Field()
    vote_items_count = scrapy.Field()
    