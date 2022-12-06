import scrapy
from .. items import ScrapyDmp9Item
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
# from twocaptcha import TwoCaptcha
import pandas as pd
import sys
import os
from selenium.webdriver.common.by import By
import json
import datetime

class PatchedForumsSpider(scrapy.Spider):
    name = 'BrainsClub'
    allowed_domains = ['scrapy.to']
    start_urls = ['https://scrapy.org/']
    
    

    def parse(self, response):
        def set_driver():
            driver = webdriver.Chrome(ChromeDriverManager().install())
            return driver
        
        def slove_APIKEY_2CAPTCHA(driver):
            element = driver.find_element(By.TAG_NAME,"img")
            element.screenshot("sample.png")
            print ("captured")
            api_key = os.getenv('APIKEY_2CAPTCHA', 'c9f2d99963edd910a020008b31730a92')
            solver = TwoCaptcha(api_key)
            try:
                result = solver.normal('sample.png', caseSensitive=1)
            except Exception as e:
                sys.exit(e)
            else:
                print (result['code'])
                #sys.exit('result: ' + str(result))
            cap_sol = driver.find_element(By.XPATH,"//input[@name='captcha']")
            cap_sol.send_keys(result['code'])
            
        def log_in(driver):
            driver.find_element(By.CSS_SELECTOR,'input[type=text]').send_keys("lesleyadrianWesly")
            driver.find_element(By.CSS_SELECTOR,'input[type=password]').send_keys("ABCabc123!@#")
            slove_APIKEY_2CAPTCHA(driver)
            driver.find_element(By.CSS_SELECTOR,'body > div > div.box-login > form > fieldset > div:nth-child(4) > div.slideExpandUp > button').click()
            
        def News(driver):
            sleep(5)
            table_rows = driver.find_element(By.CSS_SELECTOR,'tbody').find_elements(By.CSS_SELECTOR,'tr')
            for row in table_rows:
                date=row.find_elements(By.CSS_SELECTOR,'td')[0].text
                text=row.find_elements(By.CSS_SELECTOR,'td')[1].text
                extradata=json.dumps({'Main Category':driver.find_element(By.CSS_SELECTOR,'h1').text})
                count=1+len(df)
                df.loc[count,'content'] = 'Carding Marketplace'
                df.loc[count,'website_name'] =  'BrainsClub Market'
                df.loc[count,'timestamp'] = date
                df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                df.loc[count,'url'] = 'https://brainsclub.to/index.php#'
                df.loc[count,'text'] = text
                df.loc[count,'extradata'] = extradata
                df.loc[count,'post_num'] = ''
                
            return df
        def Credit_Cards(driver):
            driver.find_element(By.CSS_SELECTOR,'ul.main-navigation-menu').find_elements(By.CSS_SELECTOR,'li')[1].click()
            sleep(5)
            table_rows = driver.find_element(By.CSS_SELECTOR,'tbody').find_elements(By.CSS_SELECTOR,'tr')
            for row in table_rows[1:]:
                text='City:'+row.find_elements(By.CSS_SELECTOR,'td')[7].text
                extradata=json.dumps({'Main Category':driver.find_element(By.CSS_SELECTOR,'h1').text,'Bin':row.find_elements(By.CSS_SELECTOR,'td')[2].text,
                                 'Exp Date':row.find_elements(By.CSS_SELECTOR,'td')[3].text,'Category':row.find_elements(By.CSS_SELECTOR,'td')[4].text,
                                      'Country':row.find_elements(By.CSS_SELECTOR,'td')[5].text,'State':row.find_elements(By.CSS_SELECTOR,'td')[6].text,
                                      'Zip':row.find_elements(By.CSS_SELECTOR,'td')[8].text,
                                 'Action/Result':row.find_elements(By.CSS_SELECTOR,'td')[9].text})
                count=1+len(df)
                df.loc[count,'content'] = 'Carding Marketplace'
                df.loc[count,'website_name'] =  'BrainsClub Market'
                df.loc[count,'timestamp'] = ''
                df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                df.loc[count,'url'] = 'https://brainsclub.to/index.php#'
                df.loc[count,'text'] = text
                df.loc[count,'extradata'] = extradata
                df.loc[count,'post_num'] = ''
                
            return df
        def Dumps(driver):
            driver.find_element(By.CSS_SELECTOR,'ul.main-navigation-menu').find_elements(By.CSS_SELECTOR,'li')[2].click()
            sleep(5)
            table_rows = driver.find_element(By.CSS_SELECTOR,'tbody').find_elements(By.CSS_SELECTOR,'tr')
            for row in table_rows[1:]:
                text='Number:'+row.find_elements(By.CSS_SELECTOR,'td')[1].text
                extradata=json.dumps({'Main Category':driver.find_element(By.CSS_SELECTOR,'h1').text,'Type':row.find_elements(By.CSS_SELECTOR,'td')[2].text,
                                 'Level':row.find_elements(By.CSS_SELECTOR,'td')[3].text,'Class':row.find_elements(By.CSS_SELECTOR,'td')[4].text,
                                      'Code':row.find_elements(By.CSS_SELECTOR,'td')[5].text,'Exp Date':row.find_elements(By.CSS_SELECTOR,'td')[6].text,
                                      'Category':row.find_elements(By.CSS_SELECTOR,'td')[7].text,'Country':row.find_elements(By.CSS_SELECTOR,'td')[8].text,
                                 'Bank':row.find_elements(By.CSS_SELECTOR,'td')[9].text,'Action/Result':row.find_elements(By.CSS_SELECTOR,'td')[10].text})
                count=1+len(df)
                df.loc[count,'content'] = 'Carding Marketplace'
                df.loc[count,'website_name'] =  'BrainsClub Market'
                df.loc[count,'timestamp'] = ''
                df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                df.loc[count,'url'] = 'https://brainsclub.to/index.php#'
                df.loc[count,'text'] = text
                df.loc[count,'extradata'] = extradata
                df.loc[count,'post_num'] = ''
                
            return df
        
        def Dump_packs(driver):
            driver.find_element(By.CSS_SELECTOR,'ul.main-navigation-menu').find_elements(By.CSS_SELECTOR,'li')[4].click()
            sleep(5)
            for i in driver.find_elements(By.CSS_SELECTOR,'div.col-md-4'):
                text = i.find_element(By.CSS_SELECTOR,'div.top').text
                extradata=json.dumps({'Main Category':driver.find_element(By.CSS_SELECTOR,'h1').text,'Country':i.find_elements(By.CSS_SELECTOR,'li')[1].text,
                                     'Dumps':i.find_elements(By.CSS_SELECTOR,'li')[0].text,'Types':i.find_element(By.CSS_SELECTOR,'div.well').text,
                                     'Track':i.find_element(By.CSS_SELECTOR,'div.alert.alert-success').text,'text2':i.find_element(By.CSS_SELECTOR,'div.alert.alert-info').text,
                                     'Price':i.find_element(By.CSS_SELECTOR,'h1').text})
                count=1+len(df)
                df.loc[count,'content'] = 'Carding Marketplace'
                df.loc[count,'website_name'] =  'BrainsClub Market'
                df.loc[count,'timestamp'] = ''
                df.loc[count,'date_of_scrap'] = datetime.datetime.utcnow()
                df.loc[count,'url'] = 'https://brainsclub.to/index.php#'
                df.loc[count,'text'] = text
                df.loc[count,'extradata'] = extradata
                df.loc[count,'post_num'] = ''
            return df
        
        # bot 
        df = pd.DataFrame()
        driver=set_driver()
        driver.get('https://brainsclub.to/index.php')
        
        log_in(driver)
        
        # get data by main category
        df=News(driver)
        df=Credit_Cards(driver)
        df=Dumps(driver)
        df=Dump_packs(driver)
        driver.close()
        item = ScrapyDmp9Item()
        for row in df.iterrows():
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