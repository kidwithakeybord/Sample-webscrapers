import scrapy
import pandas as pd
import datetime

class AldiSpider(scrapy.Spider):
    name = 'aldi'
    allowed_domains = ['aldi.com.au']
    start_urls = ['https://www.aldi.com.au/en/groceries/']
    global df
    df = pd.DataFrame()
        
    def parse(self, response):
        Catogry_link=response.css('li.tab-nav--item.dropdown--list--item > a::attr(href)').getall()[:-1]
        print(Catogry_link)
        for Url in Catogry_link:
            yield scrapy.Request(url=Url,callback=self.get_product_data)
            
    def get_product_data(self, response):
        if len(response.css('div.csc-textpic-imagecolumn > a::attr(href)').getall()) > 0:
            for url in response.css('div.csc-textpic-imagecolumn > a::attr(href)').getall():
                yield scrapy.Request(url=url, callback = self.get_product_data)
        #ext data 
        for i in response.css('a.box--wrapper.ym-gl.ym-g25'):
            count=len(df)
            df.loc[count,'Date']=datetime.datetime.now().date()
            df.loc[count,'ProductName']=' '.join(i.css('div.box--description--header::text').getall()).strip()
            df.loc[count,'ProductDicription']=' '.join(i.css('div.box--description--header::text').getall()).strip()
            df.loc[count,'ProductID']=i.css('img::attr(src)').get().split('/')[-1].split('.')[0]
            df.loc[count,'ProductCatogory']=response.css('ul.breadcrumb-nav').css('span[itemprop=name]::text').getall()[2]
            df.loc[count,'ProductSubCatogory']=response.css('ul.breadcrumb-nav').css('span[itemprop=name]::text').getall()[-1]
            df.loc[count,'BreadCrum']='>'.join(response.css('ul.breadcrumb-nav').css('span[itemprop=name]::text').getall()[1:])
            try:
                df.loc[count,'ActualPrice']=i.css('div.box--price').css('span.box--value::text').get().replace('$','')+i.css('div.box--price').css('span.box--decimal::text').get()
            except:
                df.loc[count,'ActualPrice']='-'
            try:
                df.loc[count,'DiscountedPrice']=i.css('div.box--price').css('span.box--former-price::text').get().replace('$','')
            except:
                df.loc[count,'DiscountedPrice']=''
            try:
                df.loc[count,'FeatureOfPromotion']=' '.join(i.css('span.box--saveing > span::text').getall())
            except:
                df.loc[count,'FeatureOfPromotion']=''
            try:
                df.loc[count,'UnitPrice']=i.css('div.box--price').css('span.box--baseprice::text').get()
            except:
                df.loc[count,'UnitPrice']='-'
            try:
                df.loc[count,'Unit']=i.css('div.box--price').css('span.box--baseprice::text').get().split()[1]
                df.loc[count,'Size']=i.css('div.box--price').css('span.box--baseprice::text').get().split()[-1]
            except:
                df.loc[count,'Size']='-'
                df.loc[count,'Unit']='-'
            df.loc[count,'Url']=i.css('::attr(href)').get()
            
        df.to_excel('Aldi.xlsx',index=False)


