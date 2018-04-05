# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndexItem(scrapy.Item):
    tag_qiangdan = scrapy.Field()


class DetailItem(scrapy.Item):
    tag = scrapy.Field()
    pinlei = scrapy.Field()
    mingchen = scrapy.Field()
    leixing = scrapy.Field()
    yaoqiu = scrapy.Field()
    guige = scrapy.Field()
    chechang = scrapy.Field()
    chexing = scrapy.Field()
    yunfei = scrapy.Field()
    chufa = scrapy.Field()
    mudi = scrapy.Field()
    zhuangche01 = scrapy.Field()
    zhuangche02 = scrapy.Field()
    daohuo01 = scrapy.Field()
    daohuo02 = scrapy.Field()
