# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsgovItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    company = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    person = scrapy.Field()
    day = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
