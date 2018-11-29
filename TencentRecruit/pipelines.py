#-*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TencentrecruitPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        with open("tencent.json",'ab') as fileName:
             #把数据转换为字典再转换成json
            text = json.dumps(dict(item),ensure_ascii=False)+"\n"
            #写到文件中编码设置为utf-8
            fileName.write(text.encode("utf-8"))
        return item

    def close_spider(self,spider):
        pass