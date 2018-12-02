### 爬取京东图书的信息

使用scrapy_redis 实现断点续爬的功能,主要是在setting.py中加入下列代码

```python
ITEM_PIPELINES = {
    #通过RedisPipeline将item写入key为 spider.name: items的redis的list中，供后面的分布式处理item。
    'scrapy_redis.pipelines.RedisPipeline': 301
}


# 使用scarpy-redis中的调度器，在redis里面分配请求。
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#scrapy_redis.duperfilter.REPDupeFilter的去重组件，在redis数据库里做去重。
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


# 远程主机上Redis数据库的配置，有密码的话是这样配置的REDIS_URL = 'redis://user:pass@hostname:9001'
#REDIS_URL = 'redis://root@192.168.142.131:6379'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True
```

获取的数据没有存在MongoDB Or Mysql Or File中(我不会告诉你是我懒)，而是直接打印输出在了命令行。

总体实现没有难度，只是要注意在获取图书价格的时候价格并没有随着初始的URL将数据返回过来，而是所有的价格重新请求了一个新的URL，如：

![](1.png)

通过Scrapy_Redis，所有的请求和指纹都在redis数据库中，以此来判别是否爬取过

![](2.png)







### Bug

写代码过程中遇到的问题和学到的知识：

### urlparse之urljoin()的使用

例子：从例子中发现规律。

```
>>> urljoin("http://www.google.com/1/aaa.html","bbbb.html")
'http://www.google.com/1/bbbb.html'
>>> urljoin("http://www.google.com/1/aaa.html","2/bbbb.html")
'http://www.google.com/1/2/bbbb.html'
>>> urljoin("http://www.google.com/1/aaa.html","/2/bbbb.html")
'http://www.google.com/2/bbbb.html'
>>> urljoin("http://www.google.com/1/aaa.html","http://www.google.com/3/ccc.html")
'http://www.google.com/3/ccc.html'
>>> urljoin("http://www.google.com/1/aaa.html","http://www.google.com/ccc.html")
'http://www.google.com/ccc.html'
>>> urljoin("http://www.google.com/1/aaa.html","javascript:void(0)")
'javascript:void(0)'
```

参考：https://www.cnblogs.com/phil-chow/p/5347947.html

### Redis Desktop Manager的使用问题

以前也使用过这个软件，但是没有问题，能够进行redis数据库中的数据可视化。但是今天使用的时候发现在命令行中redis中有数据，可视化界面中没有，报下列错误。

**打开Redis图形化管理界面查看数据报错：scan commands not supported by redis server**

baidu了一下，发现是这是因为Redis Desktop Manager版本太高了，换一个低版本的就可以了。或升级Redis。

终于重新安装了Redis所有的一切数据该有的都有了。（奇了怪了，以前用的时候怎么可以，难道Redis Desktop Manager自动升级了？）

完。