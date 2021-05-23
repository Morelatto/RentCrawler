from datetime import datetime
from zoneinfo import ZoneInfo

import scrapy
from scrapy.loader import ItemLoader

from rent_crawler.items import ApartmentLoader, AddressLoader, PricesLoader, DetailsLoader
from rent_crawler.items import Apartment, Address, Details, TextDetails, MediaDetails

PAGE_SIZE = 36
VR_SOURCE = 'VR'


class VivaRealSpider(scrapy.Spider):
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
    headers = {'x-domain': 'www.vivareal.com.br'}
    custom_settings = {'DYNAMODB_PIPELINE_TABLE_NAME': 'vr-items'}

    def __init__(self, start_page=1, pages_to_crawl=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = start_page
        self.pages_to_crawl = pages_to_crawl

    def start_requests(self):
        page = self.start_page
        while page <= self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, from_=(page - 1) * PAGE_SIZE)
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
            loader.add_value('source', VR_SOURCE)
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
