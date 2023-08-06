from urllib.parse import urlencode, quote

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

            # Encode url parameters
            encoded_params = urlencode({k: quote(str(v)) for k, v in VR_DATA.items()})

            yield scrapy.Request(
                url=f'{self.start_url}?{encoded_params}',
                headers=self.headers,
                dont_filter=True,
                cb_kwargs=dict(page_number=page, total_pages=self.pages_to_crawl)
            )


VR_DATA = {
    'addressCity': 'São Paulo',
    'addressLocationId': 'BR>Sao Paulo>NULL>Sao Paulo>Zona Sul>Saude',
    'addressNeighborhood': 'Saúde',
    'addressState': 'São Paulo',
    'addressCountry': 'Brasil',
    'addressStreet': '',
    'addressZone': 'Zona Sul',
    'addressPointLat': '-23.607064',
    'addressPointLon': '-46.642778',
    'business': 'RENTAL',
    'facets': 'amenities',
    # 'unitTypes': 'APARTMENT,HOME,HOME,COUNTRY_HOUSE,APARTMENT,APARTMENT,APARTMENT,HOME,RESIDENTIAL_BUILDING,FARM,ALLOTMENT_LAND',
    # 'unitSubTypes': 'UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|CONDOMINIUM|UnitSubType_NONE|PENTHOUSE|FLAT|KITNET|TWO_STORY_HOUSE|UnitSubType_NONE|UnitSubType_NONE-OMINIUM|UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE',
    # 'unitTypesV3': 'APARTMENT,HOME,CONDOMINIUM,COUNTRY_HOUSE,PENTHOUSE,FLAT,KITNET,TWO_STORY_HOUSE,RESIDENTIAL_BUILDING,FARM,RESIDENTIALOTMENT_LAND',
    # 'usageTypes': 'RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIARESIDENTIAL',
    'listingType': 'USED',
    'parentId': 'null',
    'categoryPage': 'RESULT',
    # 'includeFields': 'search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,phones),facets,owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),accoid,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount))',
    'size': PAGE_SIZE,
    'from': PAGE_SIZE,
    'q': '',
    # 'developmentsSize': '5',
    '__vt': '',
    'levels': 'CITY',
    'ref': '',
    'pointRadius': '',
    'isPOIQuery': '',
}
