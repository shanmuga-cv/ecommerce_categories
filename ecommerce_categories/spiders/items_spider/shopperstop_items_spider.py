import scrapy
from ecommerce_categories.category_tree import CategoryNode
from ...items import ListingItem
import logging


class ShopperstopItemsSpider(scrapy.Spider):
    name = "shoppersstop_items"
    custom_settings = {
        'ITEM_PIPELINES': {
            'ecommerce_categories.pipelines.EcommerceListingItemsPipeline': 300,
        }
    }

    website = "shoppersstop.com"
    max_item_limit = 100 # TODO move to constructor argument to be passed from commandline with default value
    logger = logging.getLogger("ShopperstopItemsSpider")

    def start_requests(self):
        for leaf_node in CategoryNode.parse("shoppersstop_categories.json").traverse_leaf_nodes():
            yield scrapy.Request(leaf_node.link, callback=self.parse,
                                 meta={
                                     'category_hierarchy': leaf_node.category_hierarchy,
                                     'extracted_count': 0
                                 }
                                 )

    def parse(self, response):
        # parse listing page
        extracted_count = response.meta['extracted_count']
        items_links = response.xpath(
            '//ul[@id="qv-drop"]/li[@itemtype="http://schema.org/Product"]//input[@class="listProductUrl"]/@value'
        ).extract()
        for link in items_links:
            if extracted_count > self.max_item_limit:
                self.logger.info("finished extracting%(extracted_count)d out of %(max_limit)d for %(category_hierarchy)s",
                                 {
                                     'extracted_count': extracted_count,
                                     'max_limit': self.max_item_limit,
                                     'category_hierarchy': response.meta['category_hierarchy']
                                 })
                return # required number of items already crawled, stop crawling
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_product_description_page,
                meta={'category_hierarchy': response.meta['category_hierarchy']}
            )
            extracted_count += 1
        next_page_url = response.xpath('//link[@id="nexturl"]/@href').extract_first()
        self.logger.info("extracted %(extracted_count)d out of %(max_limit)d for %(category_hierarchy)s",
                         {
                             'extracted_count': extracted_count,
                             'max_limit': self.max_item_limit,
                             'category_hierarchy': response.meta['category_hierarchy']
                         })
        yield scrapy.Request(next_page_url, callback=self.parse,
                             meta={
                                 'category_hierarchy': response.meta['category_hierarchy'],
                                 'extracted_count': extracted_count
                             })

    def parse_product_description_page(self, response):
        yield ListingItem(category_tree=response.meta['category_hierarchy'], response_body=response.body, url=response.url)