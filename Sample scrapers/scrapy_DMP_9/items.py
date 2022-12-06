# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDmp9Item(scrapy.Item):
    content= scrapy.Field()
    website_name = scrapy.Field()
    timestamp = scrapy.Field()
    date_of_scrap = scrapy.Field()
    url= scrapy.Field()
    text= scrapy.Field()
    post_num= scrapy.Field()
    extradata = scrapy.Field()
    pass
