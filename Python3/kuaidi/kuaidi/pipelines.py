# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class KuaidiPipeline(object):
    def __init__(self):
        self.filename = open("kuaidiyuan_nt.txt", "wb")

    def process_item(self, item, spider):
        text = item['postmanName'].encode("utf8")+","+item['postmanCompany'].encode("utf8")+","+item['postmanTel'].encode("utf8")+","+item['postmanArea'].encode("utf8")+","+item['postmanSer'].encode("utf8")
        self.filename.write(text + ',\n')
        return item

    def close_spider(self, spider):
        self.filename.close()
