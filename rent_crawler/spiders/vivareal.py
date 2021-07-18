import scrapy

from rent_crawler.spiders import BaseVrZapSpider

PAGE_SIZE = 36


class VivaRealSpider(BaseVrZapSpider):
    name = 'vivareal'
    start_url = 'https://glue-api.vivareal.com/v2/listings?' \
                'addressCity=S%C3%A3o%20Paulo' \
                '&addressLocationId=BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo' \
                '&addressNeighborhood=' \
                '&addressState=S%C3%A3o%20Paulo' \
                '&addressCountry=Brasil' \
                '&addressStreet=' \
                '&addressZone=' \
                '&addressPointLat=-23.55052' \
                '&addressPointLon=-46.633309' \
                '&business=RENTAL' \
                '&facets=amenities' \
                '&unitTypes=APARTMENT%2CHOME%2CHOME%2CCOUNTRY_HOUSE%2CAPARTMENT%2CAPARTMENT%2CAPARTMENT%2CHOME%2CRESIDENTIAL_BUILDING%2CFARM%2CALLOTMENT_LAND' \
                '&unitSubTypes=UnitSubType_NONE%2CDUPLEX%2CLOFT%2CSTUDIO%2CTRIPLEX%7CUnitSubType_NONE%2CSINGLE_STOREY_HOUSE%2CVILLAGE_HOUSE%2CKITNET%7CCONDOMINIUM%7CUnitSubType_NONE%7CPENTHOUSE%7CFLAT%7CKITNET%7CTWO_STORY_HOUSE%7CUnitSubType_NONE%7CUnitSubType_NONE%2CCONDOMINIUM%7CUnitSubType_NONE%2CCONDOMINIUM%2CVILLAGE_HOUSE' \
                '&unitTypesV3=APARTMENT%2CHOME%2CCONDOMINIUM%2CCOUNTRY_HOUSE%2CPENTHOUSE%2CFLAT%2CKITNET%2CTWO_STORY_HOUSE%2CRESIDENTIAL_BUILDING%2CFARM%2CRESIDENTIAL_ALLOTMENT_LAND' \
                '&usageTypes=RESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL' \
                '&listingType=USED' \
                '&parentId=null' \
                '&categoryPage=RESULT' \
                '&includeFields=search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount)%2Cpage%2CseasonalCampaigns%2CfullUriFragments%2Cnearby(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))%2Cexpansion(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Cphones)%2Cfacets%2Cowners(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))' \
                '&size={size}' \
                '&from={from_}' \
                '&q=' \
                '&developmentsSize=5' \
                '&__vt=' \
                '&levels=CITY' \
                '&ref=%2Faluguel%2Fsp%2Fsao-paulo%2Fapartamento_residencial%2F' \
                '&pointRadius='
    headers = {
        'x-domain': 'www.vivareal.com.br'
    }
    custom_settings = {
        'DYNAMODB_PIPELINE_TABLE_NAME': 'vr-items',
        'ELASTICSEARCH_TYPE': 'vivareal'
    }

    def start_requests(self):
        page = self.start_page
        while page <= self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, from_=(page - 1) * PAGE_SIZE)
            yield scrapy.Request(url=req_url, headers=self.headers)
            page += 1
