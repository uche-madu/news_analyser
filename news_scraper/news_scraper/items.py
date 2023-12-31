# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    published_on = scrapy.Field()
    news_provided_by = scrapy.Field()
    headline = scrapy.Field()
    article = scrapy.Field()
    url = scrapy.Field()
