# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_tree = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()

    # Intentionally removed non-parameterized constructor to support validation.
    # This will cause problems if ItemLoader is used.
    def __init__(self, category_tree, url, website):
        if not url.startswith("http"):
            raise ValueError(f"bad url {url}")
        if not category_tree:
            raise ValueError(f"empty category_tree")
        scrapy.Item.__init__(self, category_tree=category_tree, url=url, website=website)
