import scrapy
from scrapy.http import FormRequest, Request
from ..items import ChilchilCrawlItem

class MangaSpider(scrapy.Spider):
    name = "mangas"
    # start_urls = [
    #     'https://www.chil-chil.net/goodsList/offset/0/',
    # ]

    start_urls = [
        'https://www.chil-chil.net/login/',
    ]

    def parse(self, response):
        action_loginDo = response.css('input[name="action_loginDo"]::attr(value)').get()
        token = response.css('input[name="ethna_csrf"]::attr(value)').get()
        uniqid = response.css('input[name="uniqid"]::attr(value)').get() 
        mail = 'zhanglilyzh@gmail.com'
        passwd = 'crawling'
        return FormRequest.from_response(response, formdata={
            'action_loginDo': action_loginDo,
            'ethna_csrf': token,
            'unqid': uniqid,
            'mail': mail,
            'passwd': passwd
        }, callback=self.after_login)

    def after_login(self, response):
        for i in range(1000, 2000, 50):
            yield Request(f"https://www.chil-chil.net/goodsList/offset/{i}/", callback=self.parse_page)


    def parse_page(self, response):
        for book in response.css('div.c-list'):
            booktype = book.css('span.comic').get()
            # Considering only comic works
            if booktype is not None:
                booktitle = book.css('h2.c-list_title')
                goods_id = booktitle.css('a::attr(href)')[0].get().split('/')[-2]
                goods_detail_url = f"https://www.chil-chil.net/goodsDetail/goods_id/{goods_id}/"
                yield scrapy.Request(goods_detail_url, callback=self.parse_detail)

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
        if '出版社' in field_dict:
            publisher_field = field_dict['出版社']
            item['publisher']= publisher_field.css('a::text').get() 
        if 'レーベル' in field_dict:
            label_field = field_dict['レーベル']
            item['label'] = label_field.css('span::text').get()
        if '発売日' in field_dict:
            item['sales_date'] = field_dict['発売日'].css('time::attr(datetime)').get()
        if '価格' in field_dict:
            price = field_dict['価格'].re('[0-9]+')
            if len(price) > 0:
                item['price'] = int(price[0])
        if 'ISBN' in field_dict:
            item['isbn'] = field_dict['ISBN'].css('dd::text').get()
        item['seme'] = list(set(response.css('dl.c-story_seme').css('li').css('a::text').getall()))
        item['uke'] = list(set(response.css('dl.c-story_uke').css('li').css('a::text').getall()))
        item['erodo'] = response.css('div.c-story_tag').css('dl')[0].css('dd').css('a::text').get()
        item['play'] = list(set(response.css('div.c-story_tag').css('dl')[1].css('dd').css('a::text').getall()))
        item['settei'] = list(set(response.css('div.c-story_tag').css('dl')[2].css('dd').css('a::text').getall()))
        item['tone'] = list(set(response.css('div.c-story_tag').css('dl')[3].css('dd').css('a::text').getall()))

        yield item