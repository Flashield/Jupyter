# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaidiItem(scrapy.Item):
    # 快递员
    postmanName = scrapy.Field()
    # 快递员公司
    postmanCompany = scrapy.Field()
    # 快递员电话
    postmanTel = scrapy.Field()
    # 所属区域
    postmanArea = scrapy.Field()
    # 工作地点
    postmanSer = scrapy.Field()
    # 发布时间
    postmanSerLac = scrapy.Field()
