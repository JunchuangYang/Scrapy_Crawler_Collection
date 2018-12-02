# -*- coding: utf-8 -*-
import scrapy
from copy import  deepcopy
import json
import urllib

class JdSpider(scrapy.Spider):
    name = 'JD'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item = {}
            item["b_cate"] =dt.xpath('./a/text()').extract_first(default=None) # 大分类
            em_list = dt.xpath('./following-sibling::dd[1]/em') # 当前大分类下的em标签列表
            for em in em_list:
                item["s_href"] = em.xpath('./a/@href').extract_first(default=None) # 小分类标签的url地址
                item["s_cate"] = em.xpath('./a/text()').extract_first(default=None)# 小分类名字
                # 构造小分类的请求
                if item["s_href"] is not None:
                    item["s_href"] = "https:" + item["s_href"]
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item":deepcopy(item)} #传去字典
                    )
    # 解析列表页
    def parse_book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            item["book_img"] = li.xpath('.//div[@class="p-img"]/a/img/@src').extract_first(default=None)
            if item["book_img"] is None:
                item["book_img"] = li.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img').extract_first(default=None)
            item["book_img"] = "htts:"+item["book_img"] if item["book_img"] is not None else None

            item["book_name"] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first(default=None).strip()
            # 获取作者不适用extract_first(),因为作者可能不止一个
            item["book_author"] = li.xpath('.//span[@class="author_type_1"]/a/text()').extract()
            item["book_press"] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first(default=None)
            item["book_publish_date"] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first(default=None).strip()
            # 获取价格.价格信息并没有在当前页面中显示，而是重新执行了一个url
            # 通过分析，需要获取到每本书的skuid，然后访问http://p.3.cn/prices/mgets?skuIds=J_11757834获取包含有价格信息的字符串
            item["book_sku"] = li.xpath('./div/@data-sku').extract_first(default=None)
            yield scrapy.Request(
                "http://p.3.cn/prices/mgets?skuIds=J_%s"%item["book_sku"],
                callback=self.parse_book_price,
                meta={"item":deepcopy(item)}
            )
        # 列表页翻页
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first(default=None)
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )
    def parse_book_price(self,response):
        item = response.meta["item"]
        item["book_price"] = json.loads(response.body.decode("utf-8"))[0]["op"]
        yield item










