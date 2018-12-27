# -*- coding: utf-8 -*-
import scrapy

from update.items import NovelItem


class NovelSpider(scrapy.Spider):
    """
    爬虫
    """

    # 爬虫唯一名称：使用[python -m scrapy crawl 'name']启动此爬虫
    name = 'novel_spider'
    # ？？？
    allowed_domains = ['zongheng.com']
    # 起始根链接：纵横中文网逆天邪神
    start_urls = ['http://m.zongheng.com/h5/book?bookid=408586']

    # 爬取到的链接会作为response对象传递给parse()
    def parse(self, response):
        item = NovelItem()
        # 最新章节名
        item['chapter'] = response.xpath('//span[@class="last_tit"]/text()').extract()[0]
        # 更新时间
        item['update_time'] = response.xpath('//div[@class="time"]/text()').extract()[0]

        # 将item传递给pipilines.py
        return item
