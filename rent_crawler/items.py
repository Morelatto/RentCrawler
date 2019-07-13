# -*- coding: utf-8 -*-
import re

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Identity, Join
from w3lib.html import replace_tags

parse_number = Compose(TakeFirst(), lambda string: re.findall(r'\d+|$', str(string))[0])
parse_currency = Compose(TakeFirst(), lambda price: price.split('R$ ')[-1].replace('.', ''), float)
strip = MapCompose(str.strip, replace_tags)
join = Join(', ')


class Address(Item):
    street = Field()
    district = Field()
    city = Field()


class Details(Item):
    size = Field()
    rooms = Field()
    suite = Field()
    bathrooms = Field()
    garages = Field()


class TextDetails(Item):
    description = Field(input_processor=strip, output_processor=TakeFirst())
    characteristics = Field()


class Prices(Item):
    rent = Field()
    condo = Field()
    iptu = Field()


class Apartment(Item):
    code = Field()
    address = Field(serializer=Address)
    prices = Field(serializer=Prices)
    details = Field(serializer=Details)
    text_details = Field(serializer=TextDetails)
    img_urls = Field(output_processor=Identity())
    source = Field()
    created_at = Field()
    updated_at = Field()


class AddressLoader(ItemLoader):
    default_item_class = Address
    default_input_processor = strip
    default_output_processor = TakeFirst()

    street_out = join


class DetailsLoader(ItemLoader):
    default_item_class = Details
    default_output_processor = parse_number


class PricesLoader(ItemLoader):
    default_item_class = Prices
    default_output_processor = parse_currency


class ApartmentLoader(ItemLoader):
    default_item_class = Apartment
    default_output_processor = TakeFirst()
