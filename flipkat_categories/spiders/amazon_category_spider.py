import scrapy
from ..items import CategoriesItem


class AmazonCategorySpider(scrapy.Spider):
    name = "amazon_categories"
    website = "amazon.in"

    start_urls = {
        # Men's Fashion
        'https://www.amazon.in/Mens-Clothing/b?ie=UTF8&node=1968024031&ref_=sd_allcat_sbc_mfashion_clothing', # Clothing
        'https://www.amazon.in/Mens-Tshirts-Polos/b?ie=UTF8&node=1968120031&ref_=sd_allcat_sbc_mfashion_tshirts', # T-shirts & Polos
        'https://www.amazon.in/Mens-Shirts/b?ie=UTF8&node=1968093031&ref_=sd_allcat_sbc_mfashion_shirts', # Shirts
        'https://www.amazon.in/Mens-Jeans/b?ie=UTF8&node=1968076031&ref_=sd_allcat_sbc_mfashion_jeans', # Jeans
        'https://www.amazon.in/Mens-Inner-wear/b?ie=UTF8&node=1968126031&ref_=sd_allcat_sbc_mfashion_innerwear', # Innerwear
        'https://www.amazon.in/b?ie=UTF8&node=12456568031&ref_=sd_allcat_sbc_mfashion_sportswear', # Sportswear
        'https://www.amazon.in/b?ie=UTF8&node=6172354031&ref_=sd_allcat_sbc_mfashion_designerstore', # The Designer Boutique
        'https://www.amazon.in/b?ie=UTF8&node=7459781031&ref_=sd_allcat_sbc_mfashion_all', # Men's Fashion
        'https://www.amazon.in/b?ie=UTF8&node=6648217031&ref_=sd_allcat_sbc_mfashion_af', # Amazon Fashion
        'https://www.amazon.in/mens-handloom-clothing/b?ie=UTF8&node=11969751031&ref_=sd_allcat_sbc_mfashion_handloom', # Men's Handlooms
        'https://www.amazon.in/End-of-season-sale-Clothing/b?ie=UTF8&node=4188827031&ref_=sd_allcat_sbc_mfashion_sales_deals', # Fashion Sales & Deals

        # Women's Fashion
        'https://www.amazon.in/Womens-clothing/b?ie=UTF8&node=1953602031&ref_=sd_allcat_sbc_wfashion_clothing', # Clothing
        'https://www.amazon.in/womens-western-wear/b?ie=UTF8&node=11400137031&ref_=sd_allcat_sbc_wfashion_western', # Western Wear
        'https://www.amazon.in/womens-ethnic-wear/b?ie=UTF8&node=1968253031&ref_=sd_allcat_sbc_wfashion_ethnic', # Ethnic Wear
        'https://www.amazon.in/b?ie=UTF8&node=11400136031&ref_=sd_allcat_sbc_wfashion_lingerie', # Lingerie & Nightwear
        'https://www.amazon.in/s?_encoding=UTF8&bbn=1953602031&lo=apparel&ref_=sd_allcat_sbc_wfashion_topbrands&rh=i%3Aapparel%2Cn%3A1571271031%2Cn%3A%211571272031%2Cn%3A1953602031%2Ck%3A-sunglass%20-eye%2Cp_98%3A10440597031%2Cp_n_feature_nineteen_browse-bin%3A11301357031', # Top Brands
        'https://www.amazon.in/b?ie=UTF8&node=6172354031&ref_=sd_allcat_sbc_wfashion_designerstore', # The Designer Boutique
        'https://www.amazon.in/handloom-and-handcrafts-store/b?ie=UTF8&node=11971792031&ref_=sd_allcat_sbc_wfashion_handloomstore', # Handloom & Handicraft Store
        'https://www.amazon.in/b?ie=UTF8&node=12302884031&ref_=sd_allcat_sbc_wfashion_sportswear', # Sportswear
        'https://www.amazon.in/b?ie=UTF8&node=7459780031&ref_=sd_allcat_sbc_wfashion_all', # Women's Fashion
        'https://www.amazon.in/b?ie=UTF8&node=6648217031&ref_=sd_allcat_sbc_wfashion_af', # Amazon Fashion
        'https://www.amazon.in/End-of-season-sale-Clothing/b?ie=UTF8&node=4188827031&ref_=sd_allcat_sbc_wfashion_sales_deals', # Fashion Sales & Deals

        # Toys, Baby Products, Kids' Fashion
        'https://www.amazon.in/kids-clothing/b?ie=UTF8&node=4091091031&ref_=sd_allcat_sbc_tbk_kids_clothing', # Kids' Clothing
        'https://www.amazon.in/b?ie=UTF8&node=9361420031&ref_=sd_allcat_sbc_tbk_kids_fashion', # Kids' Fashion
        'https://www.amazon.in/b?ie=UTF8&node=11987349031&ref_=sd_allcat_sbc_tbk_baby_fashion', # Baby Fashion
    }

    def parse(self, response):
        left_nav = response.xpath("//div[@id='leftNav']/h3[text()='Show results for']/following-sibling::ul[1]" )
        category_hierarchy = [ch.strip() for ch in left_nav.xpath("./li/span//text()").extract()]
        if not category_hierarchy:
            self.logger.info("category_hierarchy is empty skipping "+response.url)
            self.crawler.stats.inc_value("skipped/empty_category_hierarchy")
            return None
        record = CategoriesItem()
        record['category_tree'] = category_hierarchy
        record['url'] = response.url
        record['website'] = self.website
        yield record
        yield from [scrapy.Request(url) for url in left_nav.xpath("./ul[1]/div/li/span/a/@href").extract()]
