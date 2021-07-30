import scrapy

from rent_crawler.spiders import BaseVrZapSpider

PAGE_SIZE = 24


class ZapSpider(BaseVrZapSpider):
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
    headers = {
        'x-domain': 'www.zapimoveis.com.br'
    }
    custom_settings = {
        'ELASTICSEARCH_TYPE': name
    }

    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, from_=(page - 1) * PAGE_SIZE, page=page)
            yield scrapy.Request(url=req_url, headers=self.headers)
            page += 1
