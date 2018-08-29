# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose

parse_currency = Compose(TakeFirst(), lambda price: price.split('R$ ')[-1].replace('.', ''), float)
parse_code = MapCompose(lambda url: url.split('id-')[-1][:-1])


class Apartment(Item):
    name = Field()
    address = Field()
    size = Field()
    rooms = Field()
    bathrooms = Field()
    garages = Field()
    rent = Field()
    condo = Field()
    description = Field()
    code = Field()


class ApartmentLoader(ItemLoader):
    default_item_class = Apartment

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    rent_out = parse_currency
    condo_out = parse_currency
    code_in = parse_code
