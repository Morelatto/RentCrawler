from urllib.parse import urlencode

import scrapy

from rent_crawler.spiders import BaseVrZapSpider

PAGE_SIZE = 36


class VivaRealSpider(BaseVrZapSpider):
    name = 'viva_real'
    start_url = 'https://glue-api.vivareal.com/v2/listings'

    headers = {
        'x-domain': 'www.vivareal.com.br'
    }

    def start_requests(self):
        self.logger.info('Starting crawl of %d pages', self.pages_to_crawl)

        for page in range(self.start_page, self.start_page + self.pages_to_crawl):
            VR_DATA['from'] *= page

            yield scrapy.Request(
                url=f'{self.start_url}?{urlencode(VR_DATA)}',
                headers=self.headers,
                cb_kwargs=dict(page_number=page, total_pages=self.pages_to_crawl)
            )


VR_DATA = {
    'addressLocationId': 'BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Saude',
    'addressCountry': 'Brasil',
    'addressState': 'São Paulo',
    'addressCity': 'São Paulo',
    'addressZone': 'Zona Sul',
    'addressNeighborhood': 'Saúde',
    'addressStreet': '',
    'addressPointLat': '-23.607064',
    'addressPointLon': '-46.642778',
    'business': 'RENTAL',
    'facets': 'amenities',
    'listingType': 'USED',
    'categoryPage': 'RESULT',
    'levels': 'CITY',
    'size': PAGE_SIZE,
    'from': PAGE_SIZE,
    'usageTypes': 'RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIARESIDENTIAL',
    # 'unitTypes': 'APARTMENT,HOME,HOME,COUNTRY_HOUSE,APARTMENT,APARTMENT,APARTMENT,HOME,RESIDENTIAL_BUILDING,FARM,ALLOTMENT_LAND',
    # 'unitTypesV3': 'APARTMENT,HOME,CONDOMINIUM,COUNTRY_HOUSE,PENTHOUSE,FLAT,KITNET,TWO_STORY_HOUSE,RESIDENTIAL_BUILDING,FARM,RESIDENTIALOTMENT_LAND',
    # 'unitSubTypes': 'UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|CONDOMINIUM|UnitSubType_NONE|PENTHOUSE|FLAT|KITNET|TWO_STORY_HOUSE|UnitSubType_NONE|UnitSubType_NONE-OMINIUM|UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE',
    # 'includeFields': 'search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,phones),facets,owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),accoid,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount))',
    # 'developmentsSize': '5',
    # 'parentId': 'null',
    # 'ref': '',
    # 'pointRadius': '',
    # 'isPOIQuery': '',
    # 'q': '',
    # '__vt': '',
}
