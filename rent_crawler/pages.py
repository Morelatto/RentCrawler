import hashlib
import json
from dataclasses import dataclass

from web_poet import WebPage

from rent_crawler.items import QuintoAndarProperty, QuintoAndarDetailsLoader, QuintoAndarPricesLoader, \
    QuintoAndarTextDetails, VRZapProperty
from rent_crawler.providers import BodyJson


@dataclass
class QuintoAndarPropertyHit:
    id: str
    source: dict

    @property
    def address(self) -> dict:
        return {
            'street': self.source.get('address'),
            'district': self.source.get('neighbourhood'),
            'city': self.source.get('city'),
            'region': self.source.get('regionName')
        }

    @property
    def prices(self) -> dict:
        return {
            'rent': self.source.get('rent'),
            'iptu_and_condominium': self.source.get('iptuPlusCondominium'),
            'total': self.source.get('totalCost')
        }

    @property
    def details(self) -> dict:
        return {
            'type': self.source.get('type'),
            'area': self.source.get('area'),
            'bedrooms': self.source.get('bedrooms'),
            'parking': self.source.get('parkingSpaces')
        }

    @property
    def media(self) -> dict:
        images = ["/img/med/" + img for img in self.source.get('imageList')]
        return dict(zip(self.source.get('imageCaptionList'), images))

    def to_item(self):
        address_hash = tuple(self.address.items())
        prices_hash = tuple(self.prices.items())
        serialized_data = json.dumps(address_hash + prices_hash).encode('utf-8')
        return {'id': hashlib.md5(serialized_data).hexdigest()}


class QuintoAndarListPage(WebPage):
    def __init__(self, data: BodyJson):
        self.data = data

    @property
    def properties(self):
        for result in self.data['hits']['hits']:
            yield QuintoAndarPropertyHit(
                id=result['_id'],
                source=result['_source'],
                # url=result.url
            )

    @property
    def property_urls(self):
        return ["/imovel/" + property.id for property in self.properties]

    def to_item(self):
        for property in self.properties:
            item = QuintoAndarProperty(
                code=property.id,
                address=property.address,
                prices=property.prices,
                details=property.details,
                media=property.media,
                url=f"/imovel/{property.id}"
            )
            yield item


class QuintoAndarPropertyPage(WebPage):

    @property
    def name(self):
        return self.css("h1.CozyTypography::text").get()

    @property
    def address(self):
        district_city = self.css('div.MuiPaper-elevation1 small::text').get().split(', ')
        return {
            'street': self.css('div.MuiPaper-elevation1 h4::text').get(),
            'district': district_city[0],
            'city': district_city[1],
        }

    @property
    def prices(self):
        price_info_sel = "//p[contains(text(),'{}')]/../following-sibling::div/span/text()"
        loader = QuintoAndarPricesLoader(selector=self.css('section[data-testid="house-pricebox"]'))
        loader.add_xpath('rent', price_info_sel.format('Aluguel'))
        loader.add_xpath('condominium', price_info_sel.format('Condomínio'))
        loader.add_xpath('iptu', price_info_sel.format('IPTU'))
        loader.add_xpath('insurance', price_info_sel.format('Seguro incêndio'))
        loader.add_xpath('service_fee', price_info_sel.format('Taxa de serviço'))
        loader.add_xpath('total', price_info_sel.format('Total'))
        return loader.load_item()

    @property
    def details(self):
        main_info = self.css('div[data-testid="house-main-info"] p.CozyTypography:first-child::text').getall()
        if main_info:
            loader = QuintoAndarDetailsLoader()
            loader.add_value('area', main_info[0])
            loader.add_value('bedrooms', main_info[1])
            loader.add_value('bathrooms', main_info[2])
            loader.add_value('parking', main_info[3])
            loader.add_value('floor', main_info[4])
            loader.add_value('pet', main_info[5])
            loader.add_value('furniture', main_info[6])
            loader.add_value('subway', main_info[7])
            return loader.load_item()
        return ''

    @property
    def description(self):
        texts = self.css("div.MuiGrid-root.MuiGrid-item p.CozyTypography::text").getall()
        if len(texts) > 8:
            return texts[8]

    @property
    def owner_description(self):
        return self.xpath('//h4[text()="Descrição do proprietário"]/following-sibling::p/text()').get()

    @property
    def items(self):
        amenities_list = self.xpath('//div[@data-testid="amenities-list"]')
        return {
            "available": amenities_list.xpath(
                '//h4[text()="Itens disponíveis"]/following-sibling::div//p/text()').getall(),
            "unavailable": amenities_list.xpath(
                '//h4[text()="Itens indisponíveis"]/following-sibling::div//p/text()').getall(),
        }

    @property
    def text_details(self):
        return QuintoAndarTextDetails(
            name=self.name,
            description=self.description,
            owner_description=self.owner_description,
            items=self.items,
        )

    @property
    def media(self):
        return {"images": self.css('div.swiper-slide img::attr(data-src)').getall()}

    @property
    def publication_date(self):
        return self.css('small[data-testid="publication_date"]::text').get('')

    def to_item(self):
        item = QuintoAndarProperty(
            code=self.url.split('/')[4],
            address=self.address,
            prices=self.prices,
            details=self.details,
            text_details=self.text_details,
            media=self.media,
            url=self.url,
            publication_date=self.publication_date
        )
        return item


@dataclass
class VRZapPropertyHit:
    listing: dict
    medias: [str]
    url: str

    @property
    def id(self) -> str:
        return self.listing['id']

    @property
    def address(self) -> dict:
        address = self.listing.get('address')
        return {
            'street': [address.get('street'), address.get('streetNumber')],
            'district': address.get('neighbourhood'),
            'city': address.get('city'),
            'complement': address.get('complement'),
            'cep': address.get('zipCode'),
            'zone': address.get('zone'),
            'location': address.get('point')
        }

    @property
    def prices(self) -> dict:
        prices = self.listing['pricingInfos']
        for price in prices:
            if price.get('businessType') == 'RENTAL':
                return {
                    'rent': price.get('price'),
                    'condominium': price.get('monthlyCondoFee'),
                    'iptu': price.get('yearlyIptu'),
                    'total': [price.get('price'), price.get('monthlyCondoFee'), price.get('yearlyIptu')]
                }

    @property
    def details(self) -> dict:
        return {
            'area': self.listing.get('totalAreas') or self.listing.get('usableAreas'),
            'bedrooms': self.listing.get('bedrooms'),
            'suites': self.listing.get('suites'),
            'bathrooms': self.listing.get('bathrooms'),
            'parking': self.listing.get('parkingSpaces')
        }

    @property
    def text_details(self) -> dict:
        return {
            'description': self.listing.get('description'),
            'characteristics': self.listing.get('amenities'),
            'title': self.listing.get('title'),
            'contact': self.listing.get('advertiserContact').get('phones'),
            'type': self.listing.get('unitTypes')
        }

    @property
    def media(self) -> dict:
        return {
            'images': self.medias,
            'video': self.medias
        }

    def to_item(self):
        address_hash = tuple(self.address.items())
        prices_hash = tuple(self.prices.items())
        serialized_data = json.dumps(address_hash + prices_hash).encode('utf-8')
        return {'id': hashlib.md5(serialized_data).hexdigest()}


class VRZapListPage(WebPage):
    def __init__(self, data: BodyJson):
        self.data = data

    @property
    def properties(self):
        for result in self.data['search']['result']['listings']:
            yield VRZapPropertyHit(
                listing=result['listing'],
                medias=result['medias'],
                url=result['link']['href']
            )

    @property
    def property_urls(self):
        return [property.url for property in self.properties]

    def to_item(self):
        for property in self.properties:
            item = VRZapProperty(
                code=property.id,
                address=property.address,
                prices=property.prices,
                details=property.details,
                text_details=property.text_details,
                media=property.media,
                url=property.url
            )
            yield item
