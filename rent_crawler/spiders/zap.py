from urllib.parse import urlencode

import scrapy

from rent_crawler.spiders import BaseVrZapSpider

PAGE_SIZE = 24


class ZapSpider(BaseVrZapSpider):
    name = 'zap'
    start_url = 'https://glue-api.zapimoveis.com.br/v2/listings'

    headers = {
        'x-domain': 'www.zapimoveis.com.br'
    }

    def start_requests(self):
        self.logger.info('Starting crawl of %d pages', self.pages_to_crawl)

        for page in range(self.start_page, self.start_page + self.pages_to_crawl):
            ZAP_DATA['from'] *= page

            yield scrapy.Request(
                url=f'{self.start_url}?{urlencode(ZAP_DATA)}',
                headers=self.headers,
                dont_filter=True,
                cb_kwargs=dict(page_number=page, total_pages=self.pages_to_crawl)
            )


ZAP_DATA = {
    'addressState': 'São Paulo',
    'addressCity': 'São Paulo',
    'addressZone': '',
    'addressNeighborhood': '',
    'addressStreet': '',
    'addressLocationId': 'BR>Sao Paulo>NULL>Sao Paulo',
    'addressPointLat': '-23.55052',
    'addressPointLon': '-46.633309',
    'text': 'Apartamento',
    'business': 'RENTAL',
    'categoryPage': 'RESULT',
    'listingType': 'USED',
    'portal': 'ZAP',
    'size': PAGE_SIZE,
    'from': PAGE_SIZE,
    'usageTypes': 'RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL',
    # 'unitTypes': 'APARTMENT,HOME,HOME,COUNTRY_HOUSE,APARTMENT,APARTMENT,APARTMENT,ALLOTMENT_LAND,HOME,RESIDENTIAL_BUILDING,FARM',
    # 'unitTypesV3': 'APARTMENT,HOME,CONDOMINIUM,COUNTRY_HOUSE,PENTHOUSE,FLAT,KITNET,RESIDENTIAL_ALLOTMENT_LAND,TWO_STORY_HOUSE,RESIDENTIAL_BUILDING,FARM',
    # 'unitSubTypes': 'UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|CONDOMINIUM|UnitSubType_NONE|PENTHOUSE|FLAT|KITNET|UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE|TWO_STORY_HOUSE|UnitSubType_NONE|UnitSubType_NONE,CONDOMINIUM',
    # 'includeFields': 'search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),page,fullUriFragments,developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),superPremium(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount))',
    # 'addressAccounts': '',
    # 'addressType': 'city',
    # 'addressCountry': '',
    # 'cityWiseStreet': '1',
    # 'developmentsSize': '3',
    # 'superPremiumSize': '3',
    # 'parentId': 'null',
}
