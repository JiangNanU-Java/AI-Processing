# -*- coding: utf-8 -*-
import scrapy

from update.items import UpdateItem


class NitianspiderSpider(scrapy.Spider):
    name = 'nitianspider'
    allowed_domains = ['zongheng.com']
    start_urls = ['http://m.zongheng.com/h5/book?bookid=408586']

    def parse(self, response):
        item = UpdateItem()
        item['chapter'] = response.xpath('//span[@class="last_tit"]/text()').extract()[0]
        item['updatetime'] = response.xpath('//div[@class="time"]/text()').extract()[0]

        return item
