# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    """
    ORM实体类
    """

    # 最新章节名
    chapter = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
