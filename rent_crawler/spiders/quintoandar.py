import json

import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import RentalPropertyLoader, AddressLoader, PricesLoader, DetailsLoader
from rent_crawler.items import RentalProperty, Address, Prices, Details, MediaDetails

PAGE_SIZE = 11
SITE_URL = 'https://www.quintoandar.com.br'


class QuintoAndarSpider(scrapy.Spider):
    name = 'quintoandar'
    start_url = 'https://www.quintoandar.com.br/api/yellow-pages/v2/search'
    data = '''{{
                "filters": {{
                    "map": {{
                        "bounds_north": -23.50560423579402,
                        "bounds_south": -23.595435764205977,
                        "bounds_east": -46.58431220239025,
                        "bounds_west": -46.68230579760971,
                        "center_lat": -23.55052,
                        "center_lng": -46.633309
                    }},
                    "availability": "any",
                    "occupancy": "any",
                    "sorting": {{
                        "criteria": "relevance",
                        "order": "desc"
                    }},
                    "page_size": {page_size},
                    "offset": {offset}
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
                    "bedrooms",
                    "parkingSpaces",
                    "listingTags",
                    "yield",
                    "yieldStrategy"
                ],
                "business_context": "RENT"
                }}'''
    headers = {
        'Accept': 'application/pclick_sale.v0+json'
    }
    custom_settings = {
        'ELASTICSEARCH_TYPE': name
    }

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)

    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            json_data = json.dumps(json.loads(self.data.format(page_size=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE)))
            yield scrapy.Request(url=self.start_url, method='POST', headers=self.headers, body=json_data)
            page += 1

    def parse(self, response, **kwargs) -> RentalProperty:
        json_response = response.json()
        for result in json_response['hits']['hits']:
            source = result['_source']
            loader = RentalPropertyLoader()
            loader.add_value('code', result['_id'])
            loader.add_value('address', self.get_address(source))
            loader.add_value('prices', self.get_prices(source))
            loader.add_value('details', self.get_details(source))
            loader.add_value('media', self.get_media_details(source))
            loader.add_value('url', f"{SITE_URL}/imovel/{result['_id']}")
            loader.add_value('type', source['type'])
            yield loader.load_item()

    @classmethod
    def get_address(cls, json_source: dict) -> Address:
        address_loader = AddressLoader()
        address_loader.add_value('street', json_source.get('address'))
        address_loader.add_value('district', json_source.get('regionName'))
        address_loader.add_value('city', json_source.get('city'))
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, json_source: dict) -> Prices:
        prices_loader = PricesLoader()
        prices_loader.add_value('rent', json_source.get('rent'))
        prices_loader.add_value('iptu_and_condo', json_source.get('iptuPlusCondominium'))
        prices_loader.add_value('total', json_source.get('totalCost'))
        yield prices_loader.load_item()

    @classmethod
    def get_details(cls, json_source: dict) -> Details:
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_source.get('area'))
        details_loader.add_value('rooms', json_source.get('bedrooms'))
        details_loader.add_value('garages', json_source.get('parkingSpaces'))
        return details_loader.load_item()

    @classmethod
    def get_media_details(cls, json_source: dict) -> MediaDetails:
        media_details_loader = ItemLoader(item=MediaDetails())
        caption_list = json_source.get('imageCaptionList')
        if caption_list:
            media_list = {}
            for i, v in enumerate(json_source.get('imageList', [])):
                media_list[caption_list[i]] = f"{SITE_URL}/img/med/{v}"
            media_details_loader.add_value('images_with_caption', media_list)
        return media_details_loader.load_item()
