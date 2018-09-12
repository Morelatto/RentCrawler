# -*- coding: utf-8 -*-
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Identity, Join

import re

parse_number = Compose(TakeFirst(), lambda string: re.findall('\d+|$', string)[0])
parse_currency = Compose(TakeFirst(), lambda price: price.split('R$ ')[-1].replace('.', ''), float)
strip = MapCompose(str.strip)
join = Join(', ')


class Address(Item):
    street = Field()
    district = Field()
    city = Field()


class AddressLoader(ItemLoader):
    default_item_class = Address
    default_input_processor = strip
    default_output_processor = TakeFirst()

    street_out = join


class Details(Item):
    size = Field()
    rooms = Field()
    suite = Field()
    bathrooms = Field()
    garages = Field()


class DetailsLoader(ItemLoader):
    default_item_class = Details
    default_output_processor = parse_number


class Prices(Item):
    rent = Field()
    condo = Field()
    iptu = Field()


class PricesLoader(ItemLoader):
    default_item_class = Prices
    default_output_processor = parse_currency


class Apartment(Item):
    code = Field()
    address = Field(serializer=Address)
    details = Field(serializer=Details)
    prices = Field(serializer=Prices)
    description = Field()
    characteristics = Field()
    img_urls = Field()
    source = Field()


class ApartmentLoader(ItemLoader):
    default_item_class = Apartment
    default_output_processor = TakeFirst()

    description_in = strip
    characteristics_out = join
    img_urls_out = Identity()
