# -*- coding: utf-8 -*-
import re

from itemloaders import Identity
from itemloaders.processors import MapCompose, TakeFirst, Join, Compose
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from w3lib.html import replace_tags


def process_float_or_int(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _filter_number(value):
    number = ''.join(re.findall(r'\d', value))
    return int(number or "0")


parse_float_or_int = MapCompose(lambda x: process_float_or_int(x))
filter_number = MapCompose(lambda x: _filter_number(x))
sum_numbers = Compose(lambda v: sum(v))
strip = MapCompose(str.strip, replace_tags, lambda text: text if text != '' else None)
filter_images = MapCompose(lambda media: media.get('url') if media.get('type') == 'IMAGE' else None)
filter_videos = MapCompose(lambda media: media.get('url') if media.get('type') == 'VIDEO' else None)
format_vrzap_image_url = MapCompose(
    lambda img: img.format(width=870, height=653, action='fit-in', description='{description}'))
format_quintoandar_image_url = MapCompose(lambda img: "https://www.quintoandar.com.br/img/med/" + img)
remove_source = MapCompose(lambda location: location if location.pop('source', None) else location)
bigger_than_zero = MapCompose(parse_float_or_int, lambda v: v if v > 0 else None)


class Address(Item):
    street = Field(output_processor=Join(', '))
    district = Field()
    city = Field()


class Details(Item):
    type = Field()
    area = Field()
    bedrooms = Field()
    bathrooms = Field()
    parking = Field()


class Prices(Item):
    rent = Field()
    total = Field(output_processor=sum_numbers)


class RentalProperty(Item):
    code = Field(serializer=str)
    address = Field(serializer=Address)
    prices = Field(serializer=Prices)
    details = Field(serializer=Details)
    media = Field()
    url = Field()
    item_id = Field()


class TextDetails(Item):
    type = Field()


class AddressLoader(ItemLoader):
    default_item_class = Address
    default_input_processor = strip
    default_output_processor = TakeFirst()


class DetailsLoader(ItemLoader):
    default_item_class = Details
    default_input_processor = parse_float_or_int
    default_output_processor = TakeFirst()


class PricesLoader(ItemLoader):
    default_item_class = Prices
    default_input_processor = parse_float_or_int
    default_output_processor = TakeFirst()


class RentalPropertyLoader(ItemLoader):
    default_item_class = RentalProperty
    default_output_processor = TakeFirst()


class TextDetailsLoader(ItemLoader):
    default_item_class = TextDetails
    default_output_processor = TakeFirst()


class VRZapAddress(Address):
    complement = Field()
    cep = Field()
    zone = Field()
    location = Field(input_processor=remove_source)


class VRZapPrices(Prices):
    condominium = Field()
    iptu = Field()


class VRZapDetails(Details):
    area = Field(input_processor=bigger_than_zero)
    suites = Field()


class VRZapTextDetails(TextDetails):
    description = Field(input_processor=strip)
    characteristics = Field(output_processor=Identity())
    title = Field()
    contact = Field(output_processor=Identity())


class VRZapMediaDetails(Item):
    images = Field(input_processor=filter_images, output_processor=format_vrzap_image_url)
    video = Field(input_processor=filter_videos)


class VRZapProperty(RentalProperty):
    address = Field(serializer=VRZapAddress)
    prices = Field(serializer=VRZapPrices)
    details = Field(serializer=VRZapDetails)
    text_details = Field(serializer=VRZapTextDetails)
    media = Field(serializer=VRZapMediaDetails)
    url = Field(output_processor=Join(''))


class QuintoAndarAddress(Address):
    region = Field()


class QuintoAndarPrices(Prices):
    iptu_and_condominium = Field()
    condominium = Field()
    iptu = Field()
    insurance = Field()
    service_fee = Field()
    total = Field()


class QuintoAndarPricesLoader(ItemLoader):
    default_item_class = QuintoAndarPrices
    default_input_processor = filter_number
    default_output_processor = TakeFirst()


class QuintoAndarDetails(Details):
    floor = Field()
    pet = Field()
    furniture = Field()
    subway = Field()


class QuintoAndarDetailsLoader(ItemLoader):
    default_item_class = QuintoAndarDetails
    default_input_processor = filter_number
    default_output_processor = TakeFirst()

    floor_in = Identity()
    pet_in = Identity()
    furniture_in = Identity()
    subway_in = Identity()


class QuintoAndarTextDetails(TextDetails):
    name = Field()
    description = Field()
    owner_description = Field()
    items = Field()


class QuintoAndarProperty(RentalProperty):
    address = Field(serializer=QuintoAndarAddress)
    prices = Field(serializer=QuintoAndarPrices)
    details = Field(serializer=QuintoAndarDetails)
    text_details = Field(serializer=QuintoAndarTextDetails)
    url = Field()
    publication_date = Field()
