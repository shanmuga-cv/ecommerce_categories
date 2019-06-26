import json
import scrapy
from ..items import CategoriesItem


class FlipkartCategories(scrapy.Spider):
    name = "flipkart_categories"
    website = "flipkart.com"
    required_category_groups = ["Clothing", "Clothing Trends"]

    start_urls = [
        'https://www.flipkart.com/sitemap',
    ]

    def parse(self, response):
        for category_group in self.required_category_groups:
            clothing_category_links = response.xpath(f'//h2[a[text()="{category_group}"]]/following-sibling::div[1]/a')
            for category_link in clothing_category_links:
                category_tree = [category_group] + [category_link.xpath("text()").extract_first()]
                url = response.urljoin(category_link.xpath("@href").extract_first())
                yield CategoriesItem(category_tree, url, self.website)
                yield scrapy.Request(response.urljoin(url), callback=self.parse_filters_from_listing_page)

    def parse_filters_from_listing_page(self, response):
        js_script_data = response.xpath('//script[@id="is_script"]/text()').extract_first()
        # remove 'window.__INITIAL_STATE__ = ' from beginning and ';' from ending
        json_data = json.loads(js_script_data.strip()[27:-1])
        category_tree = json_data['pageDataV4']['browseMetadata']['storeMetaInfo']
        hierarchy = [ct['title'] for ct in category_tree]
        for x in category_tree[-1]['child']:
            category_tree = hierarchy + [x['title']]
            url = response.urljoin(x['uri'])
            yield CategoriesItem(category_tree, url, self.website)
            yield scrapy.Request(response.urljoin(x['uri']), callback=self.parse_filters_from_listing_page)
