# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoTwoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    abstract = scrapy.Field()
    chinese_tag = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    image_url = scrapy.Field()
