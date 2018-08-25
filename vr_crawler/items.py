# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class Apartment(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    size = scrapy.Field()
    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    garages = scrapy.Field()
    rent = scrapy.Field()
    condo = scrapy.Field()
    description = scrapy.Field()


class ApartmentLoader(scrapy.loader.ItemLoader):
    default_item_class = Apartment

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
