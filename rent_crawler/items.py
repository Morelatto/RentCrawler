# -*- coding: utf-8 -*-
from itemloaders import Identity
from itemloaders.processors import MapCompose, Join, Compose
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
sum_numbers = Compose(lambda v: sum(v))
strip = MapCompose(str.strip, replace_tags, lambda text: text if text != '' else None)
filter_images = MapCompose(lambda media: media.get('url') if media.get('type') == 'IMAGE' else None)
filter_videos = MapCompose(lambda media: media.get('url') if media.get('type') == 'VIDEO' else None)
format_vrzap_image_url = MapCompose(
    lambda img: img.format(width=870, height=653, action='fit-in', description='{description}'))
remove_source = MapCompose(lambda location: location if location.pop('source', None) else location)
bigger_than_zero = MapCompose(parse_float_or_int, lambda v: v if v > 0 else None)


class Address(Item):
    street = Field(output_processor=Join(', '))
    region = Field()
    neighbourhood = Field()
    city = Field()
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


class Prices(Item):
    rent = Field()
    condominium = Field()
    iptu = Field()
    total = Field(output_processor=sum_numbers)


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


class TextDetails(Item):
    type = Field()
    features = Field(output_processor=Identity())


'''VR/ZAP'''


class VRZapAddress(Address):
    complement = Field()
    zone = Field()
    location = Field(input_processor=remove_source)


class VRZapDetails(Details):
    area = Field(input_processor=bigger_than_zero)


class VRZapTextDetails(TextDetails):
    description = Field(input_processor=strip)
    title = Field()
    contact = Field(output_processor=Identity())


class VRZapMediaDetails(Item):
    images = Field(input_processor=filter_images, output_processor=format_vrzap_image_url)
    video = Field(input_processor=filter_videos)


class VRZapProperty(RentalProperty):
    address = Field(serializer=VRZapAddress)
    prices = Field(serializer=Prices)
    details = Field(serializer=VRZapDetails)
    text_details = Field(serializer=VRZapTextDetails)
    media = Field(serializer=VRZapMediaDetails)
    url = Field(output_processor=Join(''))


'''QUINTO ANDAR'''


class QuintoAndarPrices(Prices):
    iptu_and_condominium = Field()
    insurance = Field()
    service_fee = Field()
    total = Field()


class QuintoAndarDetails(Details):
    floor = Field()
    pet = Field()
    furniture = Field()
    subway = Field()


class QuintoAndarTextDetails(TextDetails):
    name = Field()
    description = Field()
    owner_description = Field()
    construction_year = Field()
    publication_date = Field()


class QuintoAndarProperty(RentalProperty):
    prices = Field(serializer=QuintoAndarPrices)
    details = Field(serializer=QuintoAndarDetails)
    text_details = Field(serializer=QuintoAndarTextDetails)
