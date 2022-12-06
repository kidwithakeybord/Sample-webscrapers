import scrapy
from .. items import ScrapyDmp9Item
import json
import datetime

class FreebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = ['freebuf.com']
    start_urls = ['http://freebuf.com/']

    def parse(self, response):
        for articalUrl in response.css('div.article-item').css('div.title-view > div > a::attr(href)').getall():
            Url='http://freebuf.com'+articalUrl
            yield scrapy.Request(url=Url,callback=self.get_artical_data)
        pass

    def get_artical_data(self, response):
        item = ScrapyDmp9Item
        
        title=response.css('span.title-span::text').get()
        text=response.css('div.content-detail').css('p::text').getall()
        timestamp=response.css('span.date::text').get().strip()
        extradata=json.dumps({'Title':title})
        
        item['content'] = 'Freebuf Forums'
        item['website_name'] = 'General Forums'
        item['timestamp'] = timestamp
        item['date_of_scrap'] = datetime.datetime.utcnow()
        item['url'] = response.url
        item['text'] = text
        item['post_num'] = post_num
        item['extradata'] = extradata
        yield item
