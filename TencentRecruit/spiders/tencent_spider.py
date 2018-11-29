# -*- coding: utf-8 -*-
import scrapy
from TencentRecruit.items import TencentrecruitItem
import re

class TencentSpiderSpider(scrapy.Spider):
    name = 'tencent_spider'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    def parse(self, response):
        #items = response.xpath('//div[@id="position"]/div[1]/table//tr')
        items = response.xpath('//*[contains(@class,"odd") or contains(@class,"even")]')
        for item in items:
            content = TencentrecruitItem()
            # 使用extract()[0]:当值为空值时会报错
            # extract_first(default=None):值为空值是返回none
            content['name'] = item.xpath('./td[1]/a/text()').extract_first(default=None)
            content['detailLink'] = "http://hr.tencent.com/" + item.xpath('./td[1]/a/@href').extract_first(default=None)
            content['positionInfo'] = item.xpath('./td[2]/text()').extract_first(default=None)
            content['peopleNumber'] = item.xpath('./td[3]/text()').extract_first(default=None)
            content['workLocation'] = item.xpath('./td[4]/text()').extract_first(default=None)
            content['publishTime'] = item.xpath('./td[5]/text()').extract_first(default=None)
            yield content

        now_page = int(re.search(r'\d+',response.url).group(0))
        end_page = int(response.xpath('//tr[@class="f"]//div[@class="right"]/div[@class="pagenav"]/a[last()-1]/text()').extract()[0])
        if now_page < end_page:
            url = re.sub(r"\d+",str(now_page+10),response.url)
            yield scrapy.Request(url, callback= self.parse)

