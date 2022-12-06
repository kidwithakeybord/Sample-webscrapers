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
        df = pd.DataFrame()
        def set_driver():
            options = webdriver.ChromeOptions()
            options.page_load_strategy = 'eager'
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            driver.maximize_window()
            return driver

        def get_data(driver,Sub_Forum_links):   
            Links=[]
            views=[]
            replays=[]
            for url in Sub_Forum_links:
                driver.get(url)
                sleep(1)
                for th in driver.find_elements(By.CSS_SELECTOR,'ol.discussionListItems > li'):
                    Links.append(th.find_element(By.CSS_SELECTOR,'h3.title').find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
                    views.append(th.find_element(By.CSS_SELECTOR,'dl.major > dd').text)
                    replays.append(th.find_element(By.CSS_SELECTOR,' dl.minor > dd').text)

            # comments data     
            for i in range(len(Links)):
                driver.get(Links[i])
                sleep(1)
                for postdata in driver.find_elements(By.CSS_SELECTOR,'#messageList > li'):
                    try:
                        try:
                            date_time_str = postdata.find_element(By.CSS_SELECTOR,'span.DateTime').get_attribute('title')
                        except:
                            date_time_str = postdata.find_element(By.CSS_SELECTOR,'abbr.DateTime').get_attribute('title')
                        try:
                            timestamp = datetime.datetime.strptime(date_time_str, '%d.%m.%Y в %H:%M')
                        except:
                            try:
                                timestamp = datetime.datetime.strptime(date_time_str, '%d-%m-%Y')
                            except:
                                timestamp = ''
                        text = postdata.find_element(By.CSS_SELECTOR,'div.messageContent').text
                        post_num = postdata.find_element(By.CSS_SELECTOR,'div.publicControls > a').text
                        url = postdata.find_element(By.CSS_SELECTOR,'div.publicControls > a').get_attribute('href')
                        User_Name=postdata.find_element(By.CSS_SELECTOR,'a.username').text
                        extradata=json.dumps({'fourm':driver.find_elements(By.CSS_SELECTOR,'span.crust')[2].find_element(By.CSS_SELECTOR,'span').text,
                                        'Sub Fourm':driver.find_elements(By.CSS_SELECTOR,'span.crust')[3].find_element(By.CSS_SELECTOR,'span').text,
                                        'views':views[i],
                                        'Replies':replays[i],
                                        'Threads subject':driver.find_element(By.CSS_SELECTOR,'div.titleBar').text,
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
                        print('comment found......')
                    except:
                        print('empty comment found......')
            return df
        
        
        driver=set_driver()
        driver.get('https://youhack.ru/')
        sleep(2)
        # part 1
        Sub_Forum_links=[]
        for F in driver.find_elements(By.CSS_SELECTOR,'ol[id=forums]'):
            for h in F.find_elements(By.CSS_SELECTOR,'h3.nodeTitle'):
                Sub_Forum_links.append( h.find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
        # part 2 get data 
        data=get_data(driver,Sub_Forum_links)
        data.to_excel('youhack.xlsx')
        
        
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
            
        
            
        
