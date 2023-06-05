import json

import scrapy

from rent_crawler.pages import QuintoAndarListPage, QuintoAndarPropertyPage

PAGE_SIZE = 11


class QuintoAndarSpider(scrapy.Spider):
    name = 'quintoandar'
    start_url = 'https://www.quintoandar.com.br/api/yellow-pages/v2/search'

    data = '''{{
                "business_context": "RENT",
                "search_query_context": "neighborhood",
                "filters": {{
                    "map": {{
                        "bounds_north": -23.60941183774316,
                        "bounds_south": -23.627263354236998,
                        "bounds_east": -46.61901770781251,
                        "bounds_west": -46.65197669218751,
                        "center_lat": -23.618337595990077,
                        "center_lng": -46.63549720000001
                    }},
                    "availability": "any",
                    "occupancy": "any",
                    "country_code": "BR",
                    "keyword_match": [
                      "neighborhood:Saúde"
                    ],
                    "sorting": {{
                        "criteria": "relevance_rent",
                        "order": "desc"
                    }},
                    "page_size": {page_size},
                    "offset": {offset},
                    "search_dropdown_value": "Saúde, São Paulo - SP, Brasil"
                }},
                "return": [
                    "id",
                    "coverImage",
                    "rent",
                    "totalCost",
                    "salePrice",
                    "iptuPlusCondominium",
                    "area",
                    "imageList",
                    "imageCaptionList",
                    "address",
                    "regionName",
                    "city",
                    "visitStatus",
                    "activeSpecialConditions",
                    "type",
                    "forRent",
                    "forSale",
                    "isPrimaryMarket",
                    "bedrooms",
                    "parkingSpaces",
                    "listingTags",
                    "yield",
                    "yieldStrategy",
                    "neighbourhood",
                    "categories"
                ]
                }}'''
    headers = {
        'Accept': 'application/pclick_sale.v0+json'
    }

    def __init__(self, start_page=1, pages_to_crawl=1, fast_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)
        self.fast_crawl = bool(int(fast_crawl))

    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            json_data = json.dumps(json.loads(self.data.format(page_size=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE)))
            yield scrapy.Request(url=self.start_url, method='POST', headers=self.headers, body=json_data,
                                 cb_kwargs=dict(page_number=page))
            page += 1

    def parse(self, response, page: QuintoAndarListPage, page_number: int):
        self.logger.info('Scrapping list page %d', page_number)
        yield from page.to_item()
        if not self.fast_crawl:
            for property_url in page.property_urls:
                yield response.follow(property_url, self.parse_property_page)

    def parse_property_page(self, response, page: QuintoAndarPropertyPage):
        self.logger.info('Scrapping property page %s', response.url)
        yield page.to_item()
