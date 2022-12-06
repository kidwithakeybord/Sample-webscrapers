import scrapy
from .. items import ScrapyDmp9Item
import datetime
import json

class PatchedForumsSpider(scrapy.Spider):
    name = 'cardvilla'
    allowed_domains = ['cardvilla.cc']
    start_urls = ['https://cardvilla.cc/']
    
    def parse(self, response):
        sub_forums_links=response.css('div.forumdata > div > div > h2 > a::attr(href)').getall()
        for url in sub_forums_links:
            yield scrapy.Request(url,callback=self.get_posts_links)
            
    def get_posts_links(self,response):
        Links=[]
        views=[]
        replies=[]
        for th in response.css('ol.stickies > li'):
            try:
                Links.append(th.css('dl[id=pagination_threadbit_9]').css('span')[-1].css('a::attr(href)').get())
            except:
                Links.append(th.css('h3.threadtitle').css('a::attr(href)').get())
            replies.append(th.css('ul.threadstats.td.alt > li > a::text')[0].get())
            views.append(th.css('ul.threadstats.td.alt > li::text')[1].get())
        
        for urlindx in range(len(Links)):
            yield scrapy.Request(url=Links[urlindx], callback=self.get_post_data, meta={'views': views[urlindx],'replays': replies[urlindx]})
     
    def get_post_data(self,response):
        item = ScrapyDmp9Item()
        views = response.meta['views']
        replays = response.meta['replays']
        
        for postdata in response.css('#posts > li'):
            timestamp = postdata.css('span.date::text').get().strip().replace(',','')
            text = ' '.join(postdata.css('div.postrow').css('blockquote ::text').getall()).strip()
            post_num = postdata.css('span.nodecontrols > a ::text').get()
            url = postdata.css('span.nodecontrols > a ::attr(href)').get()
            User_Name=postdata.css('span.usertitle > b > span::text').get()
            extradata=json.dumps({'fourm':response.css('li.navbit')[1].css('span::text').get(),
                            'Sub Fourm':response.css('li.navbit')[2].css('span::text').get(),
                            'views':views,
                            'Replies':replays,
                            'Threads subject':response.css('li.navbit')[3].css('span::text').get(),
                            'User Name':User_Name},ensure_ascii=False)
            item['content'] = 'Carding Marketplace'
            item['website_name'] = 'CardVilla Market'
            item['timestamp'] = timestamp
            item['date_of_scrap'] = datetime.datetime.utcnow()
            item['url'] = url
            item['text'] = text
            item['post_num'] = post_num
            item['extradata'] = extradata
            yield item