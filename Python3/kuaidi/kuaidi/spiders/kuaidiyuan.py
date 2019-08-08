# -*- coding: utf-8 -*-
import scrapy
from kuaidi.items import KuaidiItem



class KuaidiyuanSpider(scrapy.Spider):

    name = 'kuaidiyuan'
	
    allowed_domains = ['kuaidi.com']

    url = "http://www.kuaidi.com/kuaidiyuan/"
    
    start_urls = ["http://www.kuaidi.com/kuaidiyuan/74190.html"]
    
    offset = 74190;

    def parse(self, response):
        item = KuaidiItem()    
        item['postmanName']=response.xpath('//div[@class="top"]/h3/text()').extract()[0]
        item['postmanCompany']=response.xpath('//div[@class="top"]/p/span/text()').extract()[0]
        item['postmanTel']=response.xpath('//div[@class="top"]/p/em/text()').extract()[0]
        tempArea=response.xpath('//div[@class="postman_infor"]/dl/dd[@class="kd-ps2"]/span/text()').extract()
        for i in range(0, len(tempArea)):
            if i == 1 :
                item['postmanArea']=tempArea[i].replace(',','_')
            else:
                item['postmanArea']=""
                
        tempSer=response.xpath('//dl[@class="brnon"]/dd/span/a/text()').extract()
    	
        content = ""
        for content_one in tempSer:
            content = content+"_"+content_one
            
        item['postmanSer']=content[1:]
        
        yield item
        if self.offset < 76191:
            self.offset += 1

            # 每次处理完一页的数据之后，重新发送下一页页面请求
            # self.offset自增1，同时拼接为新的url，并调用回调函数self.parse处理Response

        yield scrapy.Request(self.url + str(self.offset)+".html", callback = self.parse)


