from datetime import datetime
from zoneinfo import ZoneInfo

import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import PropertyLoader, AddressLoader, PricesLoader, DetailsLoader
from rent_crawler.items import Property, Address, Details, TextDetails, MediaDetails


class BaseVrZapSpider(scrapy.Spider):

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = start_page
        self.pages_to_crawl = pages_to_crawl

    def parse(self, response, **kwargs) -> Property:
        json_response = response.json()
        for result in json_response['search']['result']['listings']:
            listing = result['listing']
            loader = PropertyLoader()
            loader.add_value('code', listing['id'])
            loader.add_value('address', self.get_address(listing['address']))
            loader.add_value('prices', self.get_prices(listing['pricingInfos']))
            loader.add_value('details', self.get_details(listing))
            loader.add_value('text_details', self.get_text_details(listing))
            loader.add_value('media', self.get_media_details(result['medias']))
            loader.add_value('scrapped_at', datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat())
            loader.add_value('url', result['link']['href'])
            loader.add_value('type', listing['unitTypes'])
            yield loader.load_item()

    @classmethod
    def get_address(cls, json_address: dict) -> Address:
        address_loader = AddressLoader()
        address_loader.add_value('street', json_address.get('street'))
        address_loader.add_value('street', json_address.get('streetNumber'))
        address_loader.add_value('street', json_address.get('complement'))
        address_loader.add_value('district', json_address.get('neighborhood'))
        address_loader.add_value('city', json_address.get('city'))
        address_loader.add_value('cep', json_address.get('zipCode'))
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, json_prices: list):
        for json_price in json_prices:
            prices_loader = PricesLoader()
            prices_loader.add_value('rent', json_price.get('price'))
            prices_loader.add_value('condo', json_price.get('monthlyCondoFee'))
            prices_loader.add_value('iptu', json_price.get('yearlyIptu'))
            prices_loader.add_value('total', json_price.get('rentalInfo', {}).get('monthlyRentalTotalPrice'))
            yield prices_loader.load_item()

    @classmethod
    def get_details(cls, json_apartment: dict) -> Details:
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_apartment.get('totalAreas'))
        details_loader.add_value('size', json_apartment.get('usableAreas'))
        details_loader.add_value('rooms', json_apartment.get('bedrooms'))
        details_loader.add_value('suites', json_apartment.get('suites'))
        details_loader.add_value('bathrooms', json_apartment.get('bathrooms'))
        details_loader.add_value('garages', json_apartment.get('parkingSpaces'))
        return details_loader.load_item()

    @classmethod
    def get_text_details(cls, json_apartment: dict) -> TextDetails:
        text_details_loader = ItemLoader(item=TextDetails())
        text_details_loader.add_value('description', json_apartment.get('description'))
        text_details_loader.add_value('characteristics', json_apartment.get('amenities'))
        text_details_loader.add_value('title', json_apartment.get('title'))
        text_details_loader.add_value('contact', json_apartment.get('advertiserContact').get('phones'))
        return text_details_loader.load_item()

    @classmethod
    def get_media_details(cls, json_medias: list) -> MediaDetails:
        media_details_loader = ItemLoader(item=MediaDetails())
        media_details_loader.add_value('images', json_medias)
        media_details_loader.add_value('video', json_medias)
        return media_details_loader.load_item()
