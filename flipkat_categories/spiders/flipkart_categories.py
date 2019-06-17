import scrapy
from ..items import FlipkatCategoriesItem


class FlipkartCategories(scrapy.Spider):
    name = "flipkart_categories"

    start_urls = [
        'https://www.flipkart.com/sitemap',
    ]

    def parse(self, response):
        clothing_category_links = response.xpath( '//h2[a[text()="Clothing"]]/following-sibling::div[1]/a')
        category_name = ["Clothing"]
        for category_link in clothing_category_links:
            record = FlipkatCategoriesItem()
            record['category_tree'] = category_name + [category_link.xpath("text()").extract_first()]
            record['url'] = category_link.xpath("@href").extract_first()
            yield record
            # yield scrapy.Request(record.url, callback=)
