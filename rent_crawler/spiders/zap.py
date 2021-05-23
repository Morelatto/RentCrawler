from datetime import datetime
from zoneinfo import ZoneInfo

import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import ApartmentLoader, AddressLoader, PricesLoader, DetailsLoader
from rent_crawler.items import Apartment, Address, Details, TextDetails, MediaDetails

PAGE_SIZE = 24
ZAP_SOURCE = 'Z'


class ZapSpider(scrapy.Spider):
    name = 'zap'
    start_url = 'https://glue-api.zapimoveis.com.br/v2/listings?' \
                'unitSubTypes=UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|CONDOMINIUM|UnitSubType_NONE|PENTHOUSE|FLAT|KITNET|UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE|TWO_STORY_HOUSE|UnitSubType_NONE|UnitSubType_NONE,CONDOMINIUM' \
                '&unitTypes=APARTMENT,HOME,HOME,COUNTRY_HOUSE,APARTMENT,APARTMENT,APARTMENT,ALLOTMENT_LAND,HOME,RESIDENTIAL_BUILDING,FARM' \
                '&usageTypes=RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL' \
                '&unitTypesV3=APARTMENT,HOME,CONDOMINIUM,COUNTRY_HOUSE,PENTHOUSE,FLAT,KITNET,RESIDENTIAL_ALLOTMENT_LAND,TWO_STORY_HOUSE,RESIDENTIAL_BUILDING,FARM' \
                '&text=Apartamento' \
                '&business=RENTAL' \
                '&categoryPage=RESULT' \
                '&parentId=null' \
                '&listingType=USED' \
                '&portal=ZAP' \
                '&size={size}' \
                '&from={from_}' \
                '&page={page}' \
                '&includeFields=search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29,expansion%28search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29%29,nearby%28search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29%29,page,fullUriFragments,developments%28search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29%29,superPremium%28search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29%29,owners%28search%28result%28listings%28listing%28displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status%29,account%28id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite%29,medias,accountLink,link%29%29,totalCount%29%29' \
                '&cityWiseStreet=1' \
                '&developmentsSize=3' \
                '&superPremiumSize=3' \
                '&addressCountry=' \
                '&addressState=S%C3%A3o+Paulo' \
                '&addressCity=S%C3%A3o+Paulo' \
                '&addressZone=' \
                '&addressNeighborhood=' \
                '&addressStreet=' \
                '&addressAccounts=' \
                '&addressType=city' \
                '&addressLocationId=BR%3ESao+Paulo%3ENULL%3ESao+Paulo' \
                '&addressPointLat=-23.55052' \
                '&addressPointLon=-46.633309'
    headers = {'x-domain': 'www.zapimoveis.com.br'}
    custom_settings = {'DYNAMODB_PIPELINE_TABLE_NAME': 'zap-items'}

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = start_page
        self.pages_to_crawl = pages_to_crawl

    def start_requests(self):
        page = self.start_page
        while page <= self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, from_=(page - 1) * PAGE_SIZE, page=page)
            yield scrapy.Request(url=req_url, headers=self.headers)
            page += 1

    def parse(self, response, **kwargs) -> Apartment:
        json_response = response.json()
        for result in json_response['search']['result']['listings']:
            listing = result['listing']
            loader = ApartmentLoader()
            loader.add_value('code', listing['id'])
            loader.add_value('address', self.get_address(listing['address']))
            loader.add_value('prices', self.get_prices(listing['pricingInfos']))
            loader.add_value('details', self.get_details(listing))
            loader.add_value('text_details', self.get_text_details(listing))
            loader.add_value('media', self.get_media_details(result['medias']))
            loader.add_value('source', ZAP_SOURCE)
            loader.add_value('scrapped_at', datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat())
            loader.add_value('url', result['link']['href'])
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
