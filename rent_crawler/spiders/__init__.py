import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import RentalPropertyLoader, AddressLoader, PricesLoader, DetailsLoader, TextDetailsLoader
from rent_crawler.items import VRZapRentalProperty, VRZapAddress, VRZapPrices, VRZapDetails, VRZapTextDetails, \
    VRZapMediaDetails


class BaseVrZapSpider(scrapy.Spider):
    custom_settings = {
        'ELASTICSEARCH_INDEX': 'rent-vrzap'
    }

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)

    def parse(self, response, **kwargs) -> VRZapRentalProperty:
        json_response = response.json()
        for result in json_response['search']['result']['listings']:
            listing = result['listing']
            loader = RentalPropertyLoader(item=VRZapRentalProperty())
            loader.add_value('code', listing['id'])
            loader.add_value('address', self.get_address(listing['address']))
            loader.add_value('prices', self.get_prices(listing['pricingInfos']))
            loader.add_value('details', self.get_details(listing))
            loader.add_value('text_details', self.get_text_details(listing))
            loader.add_value('media', self.get_media_details(result['medias']))
            loader.add_value('url', self.get_site_url())
            loader.add_value('url', result['link']['href'])
            yield loader.load_item()

    @classmethod
    def get_address(cls, json_address: dict) -> VRZapAddress:
        address_loader = AddressLoader(item=VRZapAddress())
        address_loader.add_value('street', json_address.get('street'))
        address_loader.add_value('street', json_address.get('streetNumber'))
        address_loader.add_value('district', json_address.get('neighborhood'))
        address_loader.add_value('city', json_address.get('city'))
        address_loader.add_value('complement', json_address.get('complement'))
        address_loader.add_value('cep', json_address.get('zipCode'))
        address_loader.add_value('zone', json_address.get('zone'))
        address_loader.add_value('location', json_address.get('point'))
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, json_prices: list) -> VRZapPrices:
        for json_price in json_prices:
            if json_price.get('businessType') == 'RENTAL':
                prices_loader = PricesLoader(item=VRZapPrices())
                prices_loader.add_value('rent', json_price.get('price'))
                prices_loader.add_value('condo', json_price.get('monthlyCondoFee'))
                prices_loader.add_value('iptu', json_price.get('yearlyIptu'))
                prices_loader.add_value('total', json_price.get('price'))
                prices_loader.add_value('total', json_price.get('monthlyCondoFee'))
                prices_loader.add_value('total', json_price.get('yearlyIptu'))
                return prices_loader.load_item()

    @classmethod
    def get_details(cls, json_listing: dict) -> VRZapDetails:
        details_loader = DetailsLoader(item=VRZapDetails())
        details_loader.add_value('size', json_listing.get('totalAreas'))
        details_loader.add_value('size', json_listing.get('usableAreas'))
        details_loader.add_value('rooms', json_listing.get('bedrooms'))
        details_loader.add_value('suites', json_listing.get('suites'))
        details_loader.add_value('bathrooms', json_listing.get('bathrooms'))
        details_loader.add_value('garages', json_listing.get('parkingSpaces'))
        return details_loader.load_item()

    @classmethod
    def get_text_details(cls, json_listing: dict) -> VRZapTextDetails:
        text_details_loader = TextDetailsLoader(item=VRZapTextDetails())
        text_details_loader.add_value('description', json_listing.get('description'))
        text_details_loader.add_value('characteristics', json_listing.get('amenities'))
        text_details_loader.add_value('title', json_listing.get('title'))
        text_details_loader.add_value('contact', json_listing.get('advertiserContact').get('phones'))
        text_details_loader.add_value('type', json_listing['unitTypes'])
        return text_details_loader.load_item()

    @classmethod
    def get_media_details(cls, json_medias: list) -> VRZapMediaDetails:
        media_details_loader = ItemLoader(item=VRZapMediaDetails())
        media_details_loader.add_value('images', json_medias)
        media_details_loader.add_value('video', json_medias)
        return media_details_loader.load_item()

    def get_site_url(self):
        raise NotImplementedError()
