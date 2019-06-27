import scrapy
from ..items import CategoriesItem


class ShoppersstopCategoriesSpider(scrapy.Spider):  # Might require throttling if many 403 http response are seen
    name = "shoppersstop_categories"
    website = "shoppersstop.com"

    def start_requests(self):
        yield from [
            # Manually extracted from "top categories" section from "Men" page (https://www.shoppersstop.com/men/c-A10)
            scrapy.Request('https://www.shoppersstop.com/men-clothing/c-A1010'),  # ["Men", "clothing"]

            # Manually extracted from "top categories" section from "Women" page
            # (https://www.shoppersstop.com/women/c-A20)
            scrapy.Request('https://www.shoppersstop.com/women-indianwear/c-A2010'),  # ["Women", "indianwear"]
            scrapy.Request('https://www.shoppersstop.com/women-westernwear/c-A2060'),  # ["Women", "Westernwear"]
        ]

    def parse(self, response):
        category_breadcrumbs = response.xpath('//ol[@class="breadcrumb"]/li//text()').extract()
        category_breadcrumbs = [x.strip() for x in category_breadcrumbs]
        if category_breadcrumbs[0].strip() == 'Home':
            category_breadcrumbs.pop(0)
        category_hierarchy = [x for x in category_breadcrumbs if x]  # remove empty strings
        yield CategoriesItem(category_hierarchy, response.url, self.website)
        sub_category_urls = [response.urljoin(x) for x in
                             response.xpath('//p[@class="heading"]/parent::div/a/@href').extract()]
        yield from (scrapy.Request(x) for x in sub_category_urls)
