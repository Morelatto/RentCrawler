import hashlib
import itertools
import json
from dataclasses import dataclass
from datetime import datetime

import pytz
from rent_crawler.items import QuintoAndarProperty, QuintoAndarTextDetails, VRZapProperty
from rent_crawler.providers import BodyJson
from web_poet import WebPage


@dataclass
class QuintoAndarPropertyHit:
    id: str
    source: dict

    @property
    def address(self) -> dict:
        return {
            'street': self.source.get('address'),
            'neighbourhood': self.source.get('neighbourhood'),
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

    def to_item(self):
        address_hash = tuple(self.address.items())
        prices_hash = tuple(self.prices.items())
        serialized_data = json.dumps(address_hash + prices_hash).encode('utf-8')
        return {'key': hashlib.sha1(serialized_data).hexdigest()}


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
                url=f"/imovel/{property.id}"
            )
            yield item


class QuintoAndarPropertyPage(WebPage):

    @property
    def name(self):
        return self.css("h1.CozyTypography::text").get()

    @property
    def address(self):
        address_data = self.json_data.get('address')
        return {
            'street': address_data.get('street'),
            'neighbourhood': address_data.get('neighborhood'),
            'city': address_data.get('city'),
            'cep': address_data.get('zipCode'),
            'lat': address_data.get('lat'),
            'lng': address_data.get('lng'),
        }

    @property
    def prices(self):
        data = self.json_data
        return {
            'rent': data.get('rentPrice'),
            'condominium': data.get('condoPrice'),
            'iptu': data.get('iptu'),
            'insurance': data.get('homeProtection'),
            'service_fee': data.get('tenantServiceFee'),
            'total': data.get('totalCost'),
        }

    @property
    def details(self):
        data = self.json_data
        return {
            'area': data.get('area'),
            'bedrooms': data.get('bedrooms'),
            'bathrooms': data.get('bathrooms'),
            'parking': data.get('parkingSpaces'),
            'floor': data.get('floor'),
            'pet': data.get('acceptsPets'),
            'furniture': data.get('hasFurniture'),
            'suites': data.get('suites'),
            'subway': data.get('isNearSubway'),
        }

    @property
    def owner_description(self):
        data = self.json_data
        return data.get('remarks')

    @property
    def features(self):
        return list(itertools.chain(
            self.amenities,
            self.comfort_commodities,
            self.practicality_commodities,
            self.installations,
        ))

    @property
    def amenities(self):
        data = self.json_data.get('amenities')
        for amenity in data:
            if amenity.get('value') == 'SIM':
                yield amenity.get('key')

    @property
    def comfort_commodities(self):
        data = self.json_data.get('comfortCommodities')
        for commodity in data:
            if commodity.get('value') == 'SIM':
                yield commodity.get('key')

    @property
    def practicality_commodities(self):
        data = self.json_data.get('practicalityCommodities')
        for commodity in data:
            if commodity.get('value') == 'SIM':
                yield commodity.get('key')

    @property
    def installations(self):
        data = self.json_data.get('installations')
        for installation in data:
            if installation.get('value') == 'SIM':
                yield installation.get('key')

    @property
    def text_details(self):
        return QuintoAndarTextDetails(
            name=self.name,
            # description=self.description,
            owner_description=self.owner_description,
            features=self.features,
            construction_year=self.json_data.get('constructionYear'),
            publication_date=self.publication_date
        )

    @property
    def media(self):
        data = self.json_data
        return {
            'images': list(self.images),
            'video': data.get('video')
        }

    @property
    def images(self, img_url='https://www.quintoandar.com.br/img/xxl/'):
        data = self.json_data
        for photo in data['photos']:
            subtitle = photo.get('subtitle')
            if subtitle is not None:
                yield {subtitle: img_url + photo['url']}

    @property
    def publication_date(self):
        def parse_date(input_date, date_fmt='%Y-%m-%dT%H:%M:%S.%f%z', tz='America/Sao_Paulo'):
            input_datetime = datetime.strptime(input_date, date_fmt)
            input_datetime = input_datetime.replace(tzinfo=pytz.utc)
            result_datetime = input_datetime.astimezone(pytz.timezone(tz))
            return result_datetime.isoformat()

        data = self.json_data
        listings = data.get('listings')
        if listings:
            return {
                'first': parse_date(listings[0].get('firstPublicationDate')),
                'last': parse_date(listings[0].get('lastPublicationDate')),
            }

    @property
    def json_data(self):
        next_data = self.css('#__NEXT_DATA__::text').get()
        json_data = json.loads(next_data)
        props_data = json_data.get('props', {})
        page_props = props_data.get('pageProps', {})
        initial_state = page_props.get('initialState', {})
        house = initial_state.get('house', {})
        return house.get('houseInfo')

    def to_item(self):
        item = QuintoAndarProperty(
            code=self.url.split('/')[4],
            address=self.address,
            prices=self.prices,
            details=self.details,
            text_details=self.text_details,
            media=self.media,
            url=self.url,
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
            'neighbourhood': address.get('neighbourhood'),
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
            'features': self.listing.get('amenities'),
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
