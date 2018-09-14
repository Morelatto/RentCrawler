from scrapy.loader import ItemLoader
from rent_crawler.items import ApartmentLoader, AddressLoader, PricesLoader, DetailsLoader, TextDetails

import json
import scrapy

TOTAL_PAGES = 277  # TODO auto detect
SIZE = 36
VR_SOURCE = 'VR'


class VivaRealSpider(scrapy.Spider):
    name = 'vivareal'
    start_url = 'https://glue-api.vivareal.com/v1/listings?' \
                  'addressCity=São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo&' \
                  'addressCountry=BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR&' \
                  'addressGeolocationLat=-23.563003,-23.571203,-23.576831,-23.569324,-23.570877,-23.573414,-23.573414,-23.562831,-23.552568,0,-23.587056,-23.591681,-23.545751,-23.571487&' \
                  'addressGeolocationLon=-46.686434,-46.68418,-46.680364,-46.656545,-46.670355,-46.672948,-46.672948,-46.646259,-46.655659,0,-46.635743,-46.62589,-46.659942,-46.630971&' \
                  'addressLocationId=BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Pinheiros,BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Paulistano,BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Europa,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardins,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim America,BR>Sao Paulo>NULL>Sao Paulo>Centro>Cerqueira Cesar,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim Paulista,BR>Sao Paulo>NULL>Sao Paulo>Centro>Bela Vista,BR>Sao Paulo>NULL>Sao Paulo>Centro>Consolacao,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Paraiso,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Vila Mariana,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Chacara Klabin,BR>Sao Paulo>NULL>Sao Paulo>Centro>Higienopolis,BR>Sao Paulo>NULL>Sao Paulo>Centro>Aclimacao&' \
                  'addressNeighborhood=Pinheiros,Jardim Paulistano,Jardim Europa,Jardins,Jardim América,Cerqueira César,Jardim Paulista,Bela Vista,Consolação,Paraíso,Vila Mariana,Chácara Klabin,Higienópolis,Aclimação&' \
                  'addressState=São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo,São Paulo&' \
                  'addressStreet=,,,,,,,,,,,,,&' \
                  'addressZone=Zona Oeste,Zona Oeste,Zona Oeste,Zona Sul,Zona Sul,Centro,Zona Sul,Centro,Centro,Zona Sul,Zona Sul,Zona Sul,Centro,Centro&' \
                  'addresses=BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Pinheiros,BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Paulistano,BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Europa,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardins,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim America,BR>Sao Paulo>NULL>Sao Paulo>Centro>Cerqueira Cesar,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim Paulista,BR>Sao Paulo>NULL>Sao Paulo>Centro>Bela Vista,BR>Sao Paulo>NULL>Sao Paulo>Centro>Consolacao,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Paraiso,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Vila Mariana,BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Chacara Klabin,BR>Sao Paulo>NULL>Sao Paulo>Centro>Higienopolis,BR>Sao Paulo>NULL>Sao Paulo>Centro>Aclimacao' \
                  'filterPricingInfoBusinessType=RENTAL&facets=amenities&filter=(address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Pinheiros" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Paulistano" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Oeste>Jardim Europa" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardins" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim America" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Centro>Cerqueira Cesar" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Jardim Paulista" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Centro>Bela Vista" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Centro>Consolacao" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Paraiso" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Vila Mariana" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Chacara Klabin" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Centro>Higienopolis" OR address.locationId:"BR>Sao Paulo>NULL>Sao Paulo>Centro>Aclimacao") AND pricingInfos.businessType:"RENTAL" AND unitTypes IN ["APARTMENT"] AND propertyType:"UNIT" AND listingType:"USED"&' \
                  'filterUnitType=APARTMENT&filterListingType=USED&' \
                  'includeFields=addresses,listingsLocation,seo,search,url,expansion,nearby,facets&' \
                  'size={size}&from={from_}&' \
                  'filterPropertyType=UNIT&q=&developmentsSize=5&__vt='

    def start_requests(self):
        for i in range(TOTAL_PAGES):
            yield scrapy.Request(url=self.start_url.format(size=SIZE, from_=SIZE * i))

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
            yield loader.load_item()

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
