import hashlib

import scrapy

from rent_crawler.pages import QuintoAndarListPage, QuintoAndarPropertyPage

PAGE_SIZE = 11

sha1 = hashlib.sha1()


class QuintoAndarSpider(scrapy.Spider):
    name = 'quinto_andar'
    start_url = 'https://www.quintoandar.com.br/api/yellow-pages/v2/search'
    headers = {
        'Accept': 'application/pclick_sale.v0+json'
    }

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        """
        Initialize the crawler with the given parameters.

        Args:
            start_page (int): The starting page number.
            pages_to_crawl (int): The number of pages to crawl.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)

    def start_requests(self):
        self.logger.info('Starting crawl of %d pages', self.pages_to_crawl)

        for page in range(self.start_page, self.start_page + self.pages_to_crawl):
            offset = (page - 1) * PAGE_SIZE
            data = QUINTO_ANDAR_DATA.format(page_size=PAGE_SIZE, offset=offset)
            yield scrapy.Request(
                url=self.start_url,
                method='POST',
                headers=self.headers,
                body=data,
                dont_filter=True,
                cb_kwargs=dict(page_number=page, total_pages=self.pages_to_crawl)
            )

    def parse(self, response: scrapy.http.Response, page: QuintoAndarListPage, **kwargs):
        self.logger.info('Scraping page %d/%d', kwargs['page_number'], kwargs['total_pages'])
        for i, d in enumerate(zip(page.property_urls, page.properties)):
            url, hit = d
            yield response.follow(
                url=url,
                callback=self.parse_property_page,
                meta=hit.to_item(),
                cb_kwargs=dict(index=i, total=len(page.property_urls))
            )

    def parse_property_page(self, response, page: QuintoAndarPropertyPage, **kwargs):
        self.logger.info('Scraping property page %d/%d', kwargs['index'], kwargs['total'])

        try:
            return page.to_item()
        except Exception as e:
            self.logger.exception("An error occurred for url %s", response.url, e)


QUINTO_ANDAR_DATA = '''{{
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
