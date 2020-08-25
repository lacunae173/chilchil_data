import scrapy
from ..items import ChilchilCrawlItem

class MangaSpider(scrapy.Spider):
    name = "mangas"
    start_urls = [
        'https://www.chil-chil.net/goodsList/offset/0/',
    ]

    def parse(self, response):
        book = response.css('div.c-list')[0]
        booktype = book.css('span.comic').get()
            # Considering only comic works
        if booktype is not None:
            booktitle = book.css('h2.c-list_title')
            goods_id = booktitle.css('a::attr(href)')[0].get().split('/')[-2]
            goods_detail_url = f"https://www.chil-chil.net/goodsDetail/goods_id/{goods_id}/"
            yield scrapy.Request(goods_detail_url, callback=self.parse_detail)
        # for book in response.css('div.c-list'):
        #     booktype = book.css('span.comic').get()
        #     # Considering only comic works
        #     if booktype is not None:
        #         booktitle = book.css('h2.c-list_title')
        #         goods_id = booktitle.css('a::attr(href)')[0].get().split('/')[-2]
        #         goods_detail_url = f"https://www.chil-chil.net/goodsDetail/goods_id/{goods_id}/"
        #         yield scrapy.Request(goods_detail_url, callback=self.parse_detail)
            
        # for book in response.css('h2.c-list_title'):
        #     goods_id = book.css('a::attr(href)')[0].get().split('/')[-2]
        #     goods_detail_url = f"https://www.chil-chil.net/goodsDetail/goods_id/{goods_id}/"
        #     yield scrapy.Request(goods_detail_url, callback=self.parse_detail)

        page_nav = response.css('li.single').css('a::attr(href)').getall()
        offset = int(response.request.url.split('/')[-2])
        next_offset = int(page_nav[1].split('/')[2])
        next_page = f"https://www.chil-chil.net/goodsList/offset/{next_offset}/" if next_offset > offset else None
        
        # if next_page is not None and next_offset < 1000:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = ChilchilCrawlItem()

        for field in item.fields:
            item.setdefault(field, None)

        item['goods_id'] = response.request.url.split('/')[-2]
        item['title'] = response.css('h1.title::text').get()

        field_names = response.css("div.c-basicdata01").css("dt::text").getall()
        fields = response.css("div.c-basicdata01").css("dd")
        field_dict = {}
        if len(field_names) == len(fields):
            field_dict = dict(zip(field_names, fields))

        if '著者' in field_dict:
            author_field = field_dict['著者']
            item['author'] = author_field.css('a::text').get() 
            item['author_id'] = author_field.css('a::attr(href)').get().split('/')[-2]
        # elif '原作' in field_dict and '作画' in field_dict:
        #     drawer_field = field_dict['作画']
        #     writer_field = field_dict['原作']
        #     item['drawer'] = drawer_field.css('a::text').get()
        #     item['drawer_id'] = drawer_field.css('a::attr(href)').get().split('/')[-2]
        #     item['writer'] = writer_field.css('a::text').get() 
        #     item['writer_id'] = writer_field.css('a::attr(href)').get().split('/')[-2]
        # if '媒体' in field_dict:
        #     category_field = field_dict['媒体']
        #     item['category'] = category_field.css('span::text').get()
        #     item['category_id'] = category_field.css("a::attr(href)").get().split('/')[-4]
        if '出版社' in field_dict:
            publisher_field = field_dict['出版社']
            item['publisher']= publisher_field.css('a::text').get() 
            item['publisher_id'] = publisher_field.css('a::attr(href)').get().split('/')[-2]
        if 'レーベル' in field_dict:
            label_field = field_dict['レーベル']
            item['label'] = label_field.css('span::text').get()
            item['label_id'] = label_field.css('a::attr(href)').get().split('/')[-2]
        if '発売日' in field_dict:
            item['sales_date'] = field_dict['発売日'].css('time::attr(datetime)').get()
        if '価格' in field_dict:
            price = field_dict['価格'].re('[0-9]+')
            if len(price) > 0:
                item['price'] = int(price[0])
        if 'ISBN' in field_dict:
            item['isbn'] = field_dict['ISBN'].css('dd::text').get()
        
        # seme tags
         # uke tags
         # erodo
         # play
         # settei
         # tone
        item['seme'] = response.css('dl.c-story_seme').css('li').css('a::text').getall()
        item['uke'] = response.css('dl.c-story_uke').css('li').css('a::text').getall()
        item['erodo'] = response.css('div.c-story_tag').css('dl')[0].css('dd').css('a::text').get()
        item['settei'] = response.css('div.c-story_tag').css('dl')[2].css('dd').css('a::text').getall()
        item['tone'] = response.css('div.c-story_tag').css('dl')[3].css('dd').css('a::text').getall()

        yield item