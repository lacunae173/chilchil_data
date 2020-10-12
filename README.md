# chilchil_data
## WARNING: Information in this repo may involve adult content, please proceed at your own risk.

This is a simple spider that crawls data from [ちるちる(chill chill)](https://www.chil-chil.net/), a japanese information website for commercial BL (boy's love) works in Japan.
The spider is built with [Scrapy](https://scrapy.org/), and crawled data is stored in MongoDB with `pymongo`.  
### Run the spider
To run the spider, first run
```
pip install -r requirement.txt
```
Go to `chilchil_crawl/` folder, and set database information in settings.py
```
MONGO_URI = "###"
MONGO_DATABASE = "###"
MONGO_COLLECTION = "###"
```
Number of items to be crawled can be specified in `spiders\manga_spider.py`  
```
# Start and end points of mangas to crawl, there are 50 works in one page
start_offset = 0;
end_offset = 50;
```
From `chilchil_crawl/` folder, run `scrapy crawl mangas`.
### Crawled data  
Some crawled data can be found in [chilchil2758.json](https://github.com/lacunae173/chilchil_data/blob/master/chilchil2758.json). These are 2758 comics with highest scores on 2020/8/28 on the website.  
Data contains  
Item | Description  
-----------|--------------------------  
goods_id | id assigned by the website
title | title of work
author | name of the author or object containing names of writer and drawer
publisher | name of publisher
label | name of label from which the work is published
sales_data | date of sale
price | price in Japanese Yen
isbn | ISBN of the book
seme | list of tags assigned to the "seme" character by the website
uke | list of tags assigned to the "uke" character by the website
erodo | extent of adult content, specified by strings in japanese
play | list of involved adult actions
settei | list of situations
tone | list of tones 
average_vote | average vote on the website
kami_percent | percentage of highest votes
score | score calculated by the website
vote_count | number of total votes
vote_items_count | list of number of votes for each rating, from high to low

