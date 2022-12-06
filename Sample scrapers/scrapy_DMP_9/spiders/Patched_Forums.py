import scrapy
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from .. items import ScrapyDmp9Item
from selenium.webdriver.common.by import By
from time import sleep
import datetime
from datetime import timedelta
import json
import pandas as pd


class PatchedForumsSpider(scrapy.Spider):
    name = 'Patched_Forums'
    allowed_domains = ['scrapy.to']
    start_urls = ['https://scrapy.org/']


    def parse(self, response):
        def set_driver():
            options = webdriver.ChromeOptions()
            options.page_load_strategy = 'eager'
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            driver.maximize_window()
            return driver
    
        def get_post_from_thread_links(Sub_Forum_links,driver):
            print('get threads....')
            links=[]
            for sfurl in Sub_Forum_links:
                driver.get(sfurl)
                sleep(2)
                for turl in driver.find_elements(By.CSS_SELECTOR,'tr.inline_row'):
                    try:
                        links.append(turl.find_element(By.CSS_SELECTOR,'span.smalltext').find_elements(By.CSS_SELECTOR,'a')[-1].get_attribute('href'))
                    except:
                        links.append(turl.find_element(By.CSS_SELECTOR,'span').find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
            return links
        
        def get_post_data_links(post_links,driver):
            print('get posts data....')
            count = 0
            for thurl in post_links:
                count=count+1
                driver.get(thurl)
                sleep(2)
                try:
                    for comments in driver.find_element(By.CSS_SELECTOR,'td[id=posts_container]').find_elements(By.CSS_SELECTOR,'div.post.classic'):
                        try:
                            date_time_str = comments.find_element(By.CSS_SELECTOR,'span.post_date').text.replace('Posted at ','').strip()
                            timestamp = datetime.datetime.strptime(date_time_str, '%d-%m-%Y, %H:%M %p')
                        except:
                            date_time_str = comments.find_element(By.CSS_SELECTOR,'span.post_date > span').get_attribute('title')
                            try:
                                timestamp = datetime.datetime.strptime(date_time_str, '%d-%m-%Y, %H:%M %p')
                            except:
                                timestamp = datetime.datetime.strptime(date_time_str, '%d-%m-%Y')
                        try:
                            text = comments.find_element(By.CSS_SELECTOR,'div.post_body.scaleimages').text
                        except:
                            text = ''
                        try:
                            post_num = comments.find_element(By.CSS_SELECTOR,'div.post_head > div > strong > a').text
                        except:
                            post_num = ''
                        try:
                            url = comments.find_element(By.CSS_SELECTOR,'div.post_head > div > strong > a').get_attribute('href')
                        except:
                            url = ''
                        try:
                            User_Name=comments.find_element(By.CSS_SELECTOR,'div.author_information').find_elements(By.CSS_SELECTOR,'strong')[1].text
                        except:
                            try:
                                User_Name=comments.find_element(By.CSS_SELECTOR,'div.author_information').find_element(By.CSS_SELECTOR,'span.largetext').text
                            except:
                                User_Name='-'  
                        #extradata 
                        try:
                            fourm=driver.find_elements(By.CSS_SELECTOR,'li[itemprop=itemListElement]')[1].text
                        except:
                            fourm='-'
                        try:
                            Subfourm=driver.find_elements(By.CSS_SELECTOR,'li[itemprop=itemListElement]')[2].text
                        except:
                            Subfourm='-'
                        try:
                            Views=driver.find_element(By.CSS_SELECTOR,'td.thead').find_elements(By.CSS_SELECTOR,'span')[-1].text
                        except:
                            Views='-'
                        try:
                            subject=comments.find_element(By.CSS_SELECTOR,'div.post_head > div > strong > a').get_attribute('title')
                        except:
                            subject='-' 
                        extradata=json.dumps({'fourm':fourm,
                                    'Sub Fourm':Subfourm,
                                    'Views':Views,
                                    'Threads subject':subject,
                                    'User Name':User_Name},ensure_ascii=False)
                        df.loc[count,'content'] = 'General Forums'
                        df.loc[count,'website_name'] = 'Patched Forums'
                        df.loc[count,'timestamp'] = timestamp
                        df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                        df.loc[count,'url'] = url
                        df.loc[count,'text'] = text
                        df.loc[count,'post_num'] = post_num
                        df.loc[count,'extradata'] = extradata
                        #print(timestamp,'\n',url,'\n',text,'\n',post_num,'\n',extradata)
                except:
                    print('no comments in this url.....',thurl)
            return df
                
        
                
        driver=set_driver()
        driver.get('https://patched.to/')
        sleep(2)
        # getting Sub_forums links
        Sub_Forum_links=[F.get_attribute('href') for F in driver.find_element(By.CSS_SELECTOR,'div[id=tab_content]').find_element(By.CSS_SELECTOR,'div[id=tab_2]').find_elements(By.CSS_SELECTOR,'a')[1:]]
        # get post from threads links
        print(len(Sub_Forum_links),'Sub_Forum_links','*'*50)
        post_links=get_post_from_thread_links(Sub_Forum_links[6:8],driver)
        print(len(post_links),'post_links','*'*50)
        df = pd.DataFrame()
        data=get_post_data_links(post_links,driver)
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
       
        driver.close()
        pass
