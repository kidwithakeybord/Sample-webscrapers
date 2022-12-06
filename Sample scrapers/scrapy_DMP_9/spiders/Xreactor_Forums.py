import scrapy
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from .. items import ScrapyDmp9Item
from selenium.webdriver.common.by import By
from time import sleep
import datetime
import pandas as pd
import json

class PatchedForumsSpider(scrapy.Spider):
    name = 'xreactor_forums'
    allowed_domains = ['scrapy.to']
    start_urls = ['https://scrapy.org/']


    def parse(self, response):
        def set_driver():
            options = webdriver.ChromeOptions()
            options.page_load_strategy = 'eager'
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            return driver
        
        def get_post_from_thread_links(Sub_Forum_links):
            print('get threads....')
            links=[]
            views=[]
            replays=[]
            for sfurl in Sub_Forum_links:
                driver.get(sfurl)
                sleep(2)
                try:
                    for Th in driver.find_elements(By.CSS_SELECTOR,'div.structItem'):
                        try:
                            links.append(Th.find_element(By.CSS_SELECTOR,'span.structItem-pageJump').find_elements(By.CSS_SELECTOR,'a')[-1].get_attribute('href'))
                        except:
                            links.append(Th.find_element(By.CSS_SELECTOR,'a[data-tp-primary=on]').get_attribute('href'))
                        replays.append(Th.find_element(By.CSS_SELECTOR,'dl.pairs.pairs--justified').text.replace('Replies\n',''))
                        views.append(Th.find_element(By.CSS_SELECTOR,'dl.pairs.pairs--justified.structItem-minor').text.replace('Views\n',''))
                except:
                    print('no threads found in this link..')
            return replays,views,links
        
        def get_post_data_links(replays,views,post_links):
            print('get posts data....')
            count=0
            for sfurl in range(len(post_links)):
                driver.get(post_links[sfurl])
                sleep(2)
                try:
                    for comments in driver.find_elements(By.CSS_SELECTOR,'article.message'):
                        timestamp = comments.find_element(By.CSS_SELECTOR,'time').get_attribute('datetime')
                        text = comments.find_element(By.CSS_SELECTOR,'div.message-content.js-messageContent').text
                        post_num = comments.find_elements(By.CSS_SELECTOR,'ul.message-attribution-opposite.message-attribution-opposite--list > li')[-1].find_element(By.CSS_SELECTOR,'a').text
                        url = comments.find_elements(By.CSS_SELECTOR,'ul.message-attribution-opposite.message-attribution-opposite--list > li')[-1].find_element(By.CSS_SELECTOR,'a').get_attribute('href')
                        try:
                            User_Name=comments.find_element(By.CSS_SELECTOR,'a.username ').text
                        except:
                            User_Name=''
                        #extradata 
                        extradata=json.dumps({'Fourm':driver.find_elements(By.CSS_SELECTOR,'li[itemprop=itemListElement]')[1].text,
                                    'Sub Fourm':driver.find_elements(By.CSS_SELECTOR,'li[itemprop=itemListElement]')[2].text,
                                    'Views':views[sfurl],
                                    'Replies':replays[sfurl],
                                    'Threads subject':driver.find_element(By.CSS_SELECTOR,'h1.p-title-value').text,
                                    'User Name':User_Name},ensure_ascii=False)
                        count=count+1
                        df.loc[count,'content'] = 'Hacking Forums'
                        df.loc[count,'website_name'] = 'XReactor Forums'
                        df.loc[count,'timestamp'] = timestamp
                        df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                        df.loc[count,'url'] = url
                        df.loc[count,'text'] = text
                        df.loc[count,'post_num'] = post_num
                        df.loc[count,'extradata'] = extradata
                except:
                    print('Url has no data........')
            return df
        
                
        driver=set_driver()
        driver.get('https://xreactor.org/')
        sleep(2)
        Sub_Forum_links=[]
        for F in driver.find_elements(By.CSS_SELECTOR,'div.block-body'):
            for h in F.find_elements(By.CSS_SELECTOR,'h3.node-title'):
                Sub_Forum_links.append( h.find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
                
        # get post from threads links
        replays,views,post_links=get_post_from_thread_links(Sub_Forum_links)
        df = pd.DataFrame()
        # get post links
        data=get_post_data_links(replays,views,post_links)
        item = ScrapyDmp9Item()
        for row in data.iterrows():
            row = row[1]
            item['content'] = row['content']
            item['website_name'] = row['website_name']
            item['timestamp'] = row['timestamp']
            item['date_of_scrap'] = row['date_of_scrap']
            item['text'] = row['text']
            item['url'] = row['url']
            item['post_num'] = row['post_num']
            item['extradata'] = row['extradata']
            yield item
        
        
        pass


