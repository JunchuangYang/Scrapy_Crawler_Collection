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
        # 数据清理，除去换行和空格
        item['title'] = item['title'].replace("\n","").replace(' ','') if item['title'] is not None else item['title']
        item['room'] = item['room'].replace("\n","").replace(' ','') if item['room'] is not None else item['room']
        item['zone'] = item['zone'].replace("\n","").replace(' ','') if item['zone'] is not None else item['zone']
        item['address'] = item['address'].replace("\n","").replace(' ','') if item['address'] is not None else item['address']
        item['money'] = item['money'].replace("\n","").replace(' ','') if item['money'] is not None else item['money']
        item['jjr'] = item['jjr'].replace("\n","").replace(' ','') if item['jjr'] is not None else item['jjr']


        with open("zufang58.json",'ab') as fileName:
            #把数据转换为字典再转换成json
            text = json.dumps(dict(item),ensure_ascii=False)+"\n"
             #写到文件中编码设置为utf-8
            fileName.write(text.encode("utf-8"))
        return item

    def close_spider(self,spider):
        pass