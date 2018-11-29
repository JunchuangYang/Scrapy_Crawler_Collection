# -*- coding: utf-8 -*-

# 可以用来对Scrapy框架的代码进行调试

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 你需要将此处的spider_name替换为你自己的爬虫名称

# 继承了CrawlSpider的zufang58的爬虫
execute(['scrapy', 'crawl', 'zufang58'])


