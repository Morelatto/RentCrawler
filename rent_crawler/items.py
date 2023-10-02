# -*- coding: utf-8 -*-
from itemloaders.processors import Compose, MapCompose, TakeFirst
from scrapy import Item, Field
from w3lib.html import replace_tags


def process_float_or_int(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


parse_float_or_int = MapCompose(lambda x: process_float_or_int(x))
strip = MapCompose(str.strip, replace_tags, lambda text: text if text != '' else None)
bigger_than_zero = MapCompose(parse_float_or_int, lambda v: v if v > 0 else None)
sum_numbers = Compose(bigger_than_zero, lambda v: sum(v))


class Address(Item):
    street = Field()
    region = Field()
    neighbourhood = Field()
    city = Field()
    state = Field()
    country = Field()
    cep = Field()
    lat = Field()
    lng = Field()


class Details(Item):
    type = Field()
    area = Field()
    bedrooms = Field()
    bathrooms = Field()
    parking = Field()
    suites = Field()


class TextDetails(Item):
    features = Field()


class Prices(Item):
    rent = Field()
    condominium = Field()
    iptu = Field()
    total = Field()


class Media(Item):
    images = Field()
    video = Field()


class RentalProperty(Item):
    code = Field(serializer=str)
    address = Field(serializer=Address)
    prices = Field(serializer=Prices)
    details = Field(serializer=Details)
    media = Field(serializer=Media)
    url = Field()


class VRZapAddress(Address):
    street = Field()
    complement = Field()
    zone = Field()


class VRZapPrice(Prices):
    rent = Field(output_processor=TakeFirst())
    condominium = Field(output_processor=TakeFirst())
    iptu = Field(output_processor=TakeFirst())
    total = Field(output_processor=sum_numbers)
    type = Field(output_processor=TakeFirst())


class VRZapDetails(Details):
    type = Field(output_processor=TakeFirst())
    area = Field(input_processor=bigger_than_zero, output_processor=TakeFirst())
    bedrooms = Field(output_processor=TakeFirst())
    bathrooms = Field(output_processor=TakeFirst())
    parking = Field(output_processor=TakeFirst())
    suites = Field(output_processor=TakeFirst())


class VRZapTextDetails(TextDetails):
    description = Field()
    title = Field()
    contact = Field()


class VRZapProperty(RentalProperty):
    address = Field(serializer=VRZapAddress)
    prices = Field(serializer=VRZapPrice)
    details = Field(serializer=VRZapDetails)
    text_details = Field(serializer=VRZapTextDetails)
    media = Field(serializer=Media)
    url = Field()


class QuintoAndarPrices(Prices):
    iptu_and_condominium = Field()
    insurance = Field()
    service_fee = Field()
    rent_total = Field()
    sale_price = Field()


class QuintoAndarDetails(Details):
    floor = Field()
    allows_pet = Field()
    is_furnished = Field()
    is_near_subway = Field()


class QuintoAndarTextDetails(TextDetails):
    name = Field()
    description = Field()
    owner_description = Field()
    construction_year = Field()
    publication_date = Field()
    for_rent = Field()
    for_sale = Field()


class QuintoAndarProperty(RentalProperty):
    prices = Field(serializer=QuintoAndarPrices)
    details = Field(serializer=QuintoAndarDetails)
    text_details = Field(serializer=QuintoAndarTextDetails)
