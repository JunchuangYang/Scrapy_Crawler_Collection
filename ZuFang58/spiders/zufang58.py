# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ZuFang58.items import Zufang58Item


class Zufang58Spider(CrawlSpider):
    name = 'zufang58'
    #allowed_domains = ['sh.58.com']
    # 开始爬取的URL
    start_urls = ['https://sh.58.com/chuzu/']
    # 从页面需要提取的url 链接(link)
    links = LinkExtractor(allow=r"sh.58.com/chuzu/pn\d+")
    # 设置解析link的规则，callback是指解析link返回的响应数据的的方法
    rules = (
        Rule(links, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        解析响应的数据，获取需要的数据字段
        :param response: 响应的数据
        :return:
        """
        items = response.xpath('//ul[@class="listUl"]/li[@logr]')
        for item in items:
            content = Zufang58Item()
            # 标题
            content['title'] = item.xpath('./div[@class ="des"]/h2/a/text()').extract_first(default=None)
            # 房间
            content['room'] = (item.xpath('./div[@class ="des"]/p[@class="room strongbox"]/text()').extract_first(default=None))
            # 区域
            content['zone'] = item.xpath('./div[@class ="des"]/p[@class="add"]/a[1]/text()').extract_first(default=None)
            # 地址
            content['address'] = item.xpath('./div[@class ="des"]/p[@class="add"]/a[last()]/text()').extract_first(default=None)
            # 价格
            content['money'] = item.xpath('.//div[@class="money"]/b/text()').extract_first(default=None)+"元/月   "
            # 发布信息的类型，品牌公寓，经纪人，个人
            detail = item.xpath('.//div[@class="jjr"]')
            jjr1=detail.xpath('./text()').extract_first(default=None)
            jjr2=detail.xpath('.//span[@class="jjr_par_dp"]/text()').extract_first(default=None)
            jjr3=detail.xpath('//span[@class="listjjr"]/text()').extract_first(default=None)
            content['jjr']=' '
            if jjr1 is not None:
                content['jjr']+=jjr1
            if jjr2 is not None:
                content['jjr']+=jjr2
            if jjr3 is not None:
                content['jjr']+=jjr3

            yield content




