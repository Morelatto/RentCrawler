from rent_crawler.items import PricesLoader, AddressLoader, DetailsLoader, ApartmentLoader

import json
import scrapy

# TODO auto detect
TOTAL_PAGES = 10
SIZE = 36


class VivaRealSpider(scrapy.Spider):
    name = 'vivareal'
    listing_url = 'https://glue-api.vivareal.com/v1/listings?' \
                  'addressCity=S%C3%A3o%20Paulo&' \
                  'addressCountry=BR&' \
                  'addressGeolocationLat=-23.550519&' \
                  'addressGeolocationLon=-46.633309&' \
                  'addressLocationId=BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo&' \
                  'addressNeighborhood=&' \
                  'addressState=S%C3%A3o%20Paulo&' \
                  'addressStreet=&' \
                  'addressZone=&' \
                  'addresses=BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo&' \
                  'filterPricingInfoBusinessType=RENTAL&' \
                  'facets=amenities&' \
                  'filter=((address.locationId%20LIKE%20%22BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo%3E%25%22%20OR%20address.locationId%3A%22BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo%22))%20AND%20pricingInfos.businessType%3A%22RENTAL%22%20AND%20unitTypes%20IN%20%5B%22APARTMENT%22%5D%20AND%20propertyType%3A%22UNIT%22%20AND%20listingType%3A%22USED%22&' \
                  'filterUnitType=APARTMENT&' \
                  'filterListingType=USED&' \
                  'includeFields=addresses%2ClistingsLocation%2Cseo%2Csearch%2Curl%2Cexpansion%2Cnearby&' \
                  'size={size}&' \
                  'from={from_}&' \
                  'filterPropertyType=UNIT&' \
                  'q=&' \
                  'developmentsSize=5&' \
                  '__vt='

    def start_requests(self):
        for i in range(TOTAL_PAGES):
            yield scrapy.Request(url=self.listing_url.format(size=SIZE, from_=SIZE * i))

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for json_apartment in json_response['search']['result']['listings']:
            json_apartment = json_apartment['listing']
            loader = ApartmentLoader()
            loader.add_value('code', json_apartment['id'])
            loader.add_value('address', self.get_address(json_apartment['address']))
            loader.add_value('details', self.get_details(json_apartment))
            loader.add_value('prices', self.get_prices(json_apartment['pricingInfos'][0]))
            loader.add_value('description', json_apartment['description'])
            loader.add_value('characteristics', json_apartment['amenities'])
            loader.add_value('img_urls', [image.format(width=600, height=900, action='action')
                                          for image in json_apartment['images']])
            loader.add_value('source', 'VR')

            yield loader.load_item()

    @classmethod
    def get_address(cls, json_address):
        address_loader = AddressLoader()
        address_loader.add_value('street', json_address.get('street'))
        address_loader.add_value('street', json_address.get('streetNumber'))
        address_loader.add_value('district', json_address['neighborhood'])
        address_loader.add_value('city', json_address['city'])
        return address_loader.load_item()

    @classmethod
    def get_details(cls, json_apartment):
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_apartment['totalAreas'])
        details_loader.add_value('rooms', json_apartment['bedrooms'])
        details_loader.add_value('suite', json_apartment['suites'])
        details_loader.add_value('bathrooms', json_apartment['bathrooms'])
        details_loader.add_value('garages', json_apartment['parkingSpaces'])
        return details_loader.load_item()

    @classmethod
    def get_prices(cls, json_prices):
        prices_loader = PricesLoader()
        prices_loader.add_value('rent', json_prices.get('price'))
        prices_loader.add_value('condo', json_prices.get('monthlyCondoFee'))
        prices_loader.add_value('iptu', json_prices.get('yearlyIptu'))
        return prices_loader.load_item()
