import json
import math

import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import ApartmentLoader, AddressLoader, PricesLoader, DetailsLoader, TextDetails

PAGE_SIZE = 36
VR_SOURCE = 'VR'


class VivaRealSpider(scrapy.Spider):
    MAX_PAGE = None

    name = 'vivareal'
    start_url = 'https://glue-api.vivareal.com/v1/listings?filter={filter}&size={size}&from={from_}'

    def __init__(self, location_id, **kwargs):
        super().__init__(**kwargs)
        self.filter = '(address.locationId:"{}") ' \
                      'AND pricingInfos.businessType:"RENTAL" ' \
                      'AND unitTypes IN ["APARTMENT"] ' \
                      'AND propertyType:"UNIT" ' \
                      'AND listingType:"USED"'.format(location_id)

    def start_requests(self):
        page = 0
        while True:
            yield scrapy.Request(self.start_url.format(filter=self.filter, size=PAGE_SIZE, from_=PAGE_SIZE * page))
            page += 1
            if self.MAX_PAGE and page > self.MAX_PAGE:
                break

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for json_apartment in json_response['search']['result']['listings']:
            json_apartment = json_apartment['listing']
            loader = ApartmentLoader()
            loader.add_value('code', json_apartment['id'])
            loader.add_value('address', self.get_address(json_apartment['address']))
            loader.add_value('prices', self.get_prices(json_apartment['pricingInfos']))
            loader.add_value('details', self.get_details(json_apartment))
            loader.add_value('text_details', self.get_text_details(json_apartment))
            loader.add_value('img_urls', self.get_img_urls(json_apartment['images']))
            loader.add_value('source', VR_SOURCE)
            loader.add_value('created_at', json_apartment.get('createdAt'))
            loader.add_value('updated_at', json_apartment.get('updatedAt'))
            yield loader.load_item()

        if not self.MAX_PAGE:
            self.MAX_PAGE = math.ceil(json_response['search']['totalCount'] / PAGE_SIZE)

    @classmethod
    def get_address(cls, json_address):
        address_loader = AddressLoader()
        address_loader.add_value('street', json_address.get('street'))
        address_loader.add_value('street', json_address.get('streetNumber'))
        address_loader.add_value('district', json_address.get('neighborhood'))
        address_loader.add_value('city', json_address.get('city'))
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, json_prices):
        json_prices = json_prices[0]
        prices_loader = PricesLoader()
        prices_loader.add_value('rent', json_prices.get('price'))
        prices_loader.add_value('condo', json_prices.get('monthlyCondoFee'))
        prices_loader.add_value('iptu', json_prices.get('yearlyIptu'))
        return prices_loader.load_item()

    @classmethod
    def get_details(cls, json_apartment):
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_apartment.get('totalAreas'))
        details_loader.add_value('rooms', json_apartment.get('bedrooms'))
        details_loader.add_value('suite', json_apartment.get('suites'))
        details_loader.add_value('bathrooms', json_apartment.get('bathrooms'))
        details_loader.add_value('garages', json_apartment.get('parkingSpaces'))
        return details_loader.load_item()

    @classmethod
    def get_text_details(cls, json_apartment):
        text_details_loader = ItemLoader(item=TextDetails())
        text_details_loader.add_value('description', json_apartment.get('description'))
        text_details_loader.add_value('characteristics', json_apartment.get('amenities'))
        return text_details_loader.load_item()

    @classmethod
    def get_img_urls(cls, json_images):
        return [img_url.format(width=600, height=900, action='action') for img_url in json_images]
