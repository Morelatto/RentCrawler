# -*- coding: utf-8 -*-
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Identity, Join

import re

parse_number = Compose(TakeFirst(), lambda string: re.findall('\d+|$', str(string))[0])
parse_currency = Compose(TakeFirst(), lambda price: price.split('R$ ')[-1].replace('.', ''), float)
strip = MapCompose(str.strip)
join = Join(', ')


class Address(Item):
    street = Field(output_processor=join)
    district = Field()
    city = Field()


class AddressLoader(ItemLoader):
    default_item_class = Address
    default_input_processor = strip
    default_output_processor = TakeFirst()


class Details(Item):
    size = Field()
    rooms = Field()
    suite = Field()
    bathrooms = Field()
    garages = Field()


class DetailsLoader(ItemLoader):
    default_item_class = Details
    default_output_processor = parse_number


class TextDetails(Item):
    description = Field(input_processor=strip, output_processor=TakeFirst())
    characteristics = Field(output_processor=join)


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
    prices = Field(serializer=Prices)
    details = Field(serializer=Details)
    text_details = Field(serializer=TextDetails)
    img_urls = Field(output_processor=Identity())
    source = Field()


class ApartmentLoader(ItemLoader):
    default_item_class = Apartment
    default_output_processor = TakeFirst()
