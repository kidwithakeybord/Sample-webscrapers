import scrapy
from .. items import ScrapyDmp9Item
import datetime
import json
import pandas as pd

class PatchedForumsSpider(scrapy.Spider):
    name = 'youhack_forums'
    allowed_domains = ['youhack.ru']
    start_urls = ['https://youhack.ru/']
    global df
    df = pd.DataFrame()
    

    def parse(self, response):
        sub_forums_links=response.css('ol[id=forums]').css('h3.nodeTitle').css('a::attr(href)').getall()
        for url in sub_forums_links:
            yield scrapy.Request('https://youhack.ru/'+url,callback=self.get_posts_links)
            
    def get_posts_links(self,response):
        Links=[]
        views=[]
        replays=[]
        for th in response.css('ol.discussionListItems > li'):
            Links.append('https://youhack.ru/'+th.css('h3.title').css('a::attr(href)').get())
            views.append(th.css('dl.major > dd::text').get())
            replays.append(th.css(' dl.minor > dd::text').get())
        
        for urlindx in range(len(Links)):
            yield scrapy.Request(url=Links[urlindx], callback=self.get_post_data, meta={'views': views[urlindx],'replays': replays[urlindx]})
        
        
    def get_post_data(self,response):
        item = ScrapyDmp9Item()
        views = response.meta['views']
        replays = response.meta['replays']
        
        for postdata in response.css('#messageList > li'):
            try:
                date_time_str = postdata.css('span.DateTime::attr(title)').get()
            except:
                date_time_str = postdata.css('abbr.DateTime::attr(title)').get()
            try:
                timestamp = datetime.datetime.strptime(date_time_str, '%d.%m.%Y в %H:%M')
            except:
                try:
                    timestamp = datetime.datetime.strptime(date_time_str, '%d-%m-%Y')
                except:
                    timestamp = ''
            text = ' '.join(postdata.css('div.messageContent > article').css('blockquote ::text').getall()).strip()
            post_num = postdata.css('div.publicControls > a ::text').get()
            url = 'https://youhack.ru/'+postdata.css('div.publicControls > a ::attr(href)').get()
            User_Name=postdata.css('a.username ::text').get()
            extradata=json.dumps({'fourm':response.css('span.crust')[2].css('span::text').extract()[1],
                            'Sub Fourm':response.css('span.crust')[3].css('span::text').extract()[1],
                            'views':views,
                            'Replies':replays,
                            'Threads subject':response.css('div.titleBar').css('h1::text').get(),
                            'User Name':User_Name},ensure_ascii=False)
            count=len(df)+1
            df.loc[count,'content'] = 'Hacking Forums'
            df.loc[count,'website_name'] =  'YouHack Forums'
            df.loc[count,'timestamp'] = timestamp
            df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
            df.loc[count,'url'] = url
            df.loc[count,'text'] = text
            df.loc[count,'post_num'] = post_num
            df.loc[count,'extradata'] = extradata
           
            item['content'] = 'Hacking Forums'
            item['website_name'] = 'BrainsClub Market'
            item['timestamp'] = timestamp
            item['date_of_scrap'] = datetime.datetime.utcnow()
            item['url'] = url
            item['text'] = text
            item['post_num'] = post_num
            item['extradata'] = extradata
            yield item
        df.to_excel('youhack.xlsx')
            
        
            
        
