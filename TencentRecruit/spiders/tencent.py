# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentRecruit.items import TencentrecruitItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0']
    page_lx = LinkExtractor(allow=r"start=\d+")#position.php?&start=0
    rules = (
        Rule(page_lx, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
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
    # parse() 方法不需要重写
    # def parse(self, response):
    #     pass