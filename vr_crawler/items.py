# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_district(address):
    address_list = address.split(' - ')
    district = address_list[0] if len(address_list) < 3 else address_list[1]
    return district.replace(', São Paulo', '')


def get_street(address):
    address_list = address.split(' - ')
    return '' if len(address_list) < 3 else address_list[0]


parse_district = Compose(TakeFirst(), get_district)
parse_street = Compose(TakeFirst(), get_street)
parse_city = Compose(TakeFirst(), lambda address: address.split(' - ')[-1])
parse_number = Compose(TakeFirst(), lambda number: int(number) if number.isdigit() else 0)
parse_currency = Compose(TakeFirst(), lambda price: price.split('R$ ')[-1].replace('.', ''), float)
parse_code = MapCompose(lambda url: url.split('id-')[-1][:-1])
strip = MapCompose(str.strip)


class Address(Item):
    street = Field()
    district = Field()
    city = Field()


class Apartment(Item):
    name = Field()
    address = Field(serializer=Address)
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

    default_input_processor = strip
    default_output_processor = TakeFirst()

    address_in = TakeFirst()
    rooms_out = parse_number
    bathrooms_out = parse_number
    garages_out = parse_number
    rent_out = parse_currency
    condo_out = parse_currency
    code_in = parse_code


class AddressLoader(ItemLoader):
    default_item_class = Address

    default_input_processor = strip
    default_output_processor = TakeFirst()

    street_out = parse_street
    district_out = parse_district
    city_out = parse_city
