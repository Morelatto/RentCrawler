# -*- coding: utf-8 -*-
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import replace_tags


def process_float_or_int(value):
    try:
        return eval(value)
    except:
        return value


parse_float_or_int = MapCompose(lambda x: process_float_or_int(x))
strip = MapCompose(str.strip, replace_tags, lambda text: text if text != '' else None)
join = Join(', ')
filter_images = MapCompose(lambda media: media.get('url') if media.get('type') == 'IMAGE' else None)
filter_videos = MapCompose(lambda media: media.get('url') if media.get('type') == 'VIDEO' else None)
format_image_url = MapCompose(lambda img: img.format(width=870, height=653, action='fit-in'))


class Address(Item):
    street = Field(output_processor=join)
    district = Field()
    city = Field()
    cep = Field()


class AddressLoader(ItemLoader):
    default_item_class = Address
    default_input_processor = strip
    default_output_processor = TakeFirst()


class Prices(Item):
    rent = Field()
    condo = Field()
    iptu = Field()
    iptu_and_condo = Field()
    total = Field()


class PricesLoader(ItemLoader):
    default_item_class = Prices
    default_input_processor = parse_float_or_int
    default_output_processor = TakeFirst()


class Details(Item):
    size = Field()
    rooms = Field()
    suites = Field()
    bathrooms = Field()
    garages = Field()


class DetailsLoader(ItemLoader):
    default_item_class = Details
    default_input_processor = parse_float_or_int
    default_output_processor = TakeFirst()


class TextDetails(Item):
    description = Field(input_processor=strip, output_processor=TakeFirst())
    characteristics = Field()
    title = Field(output_processor=TakeFirst())
    contact = Field()


class MediaDetails(Item):
    images = Field(input_processor=filter_images, output_processor=format_image_url)
    video = Field(input_processor=filter_videos)
    images_with_caption = Field()


class RentalProperty(Item):
    code = Field()
    address = Field(serializer=Address)
    prices = Field(serializer=Prices)
    details = Field(serializer=Details)
    text_details = Field(serializer=TextDetails)
    media = Field(serializer=MediaDetails)
    scrapped_at = Field()
    timestamp = Field()
    url = Field()
    type = Field(output_processor=TakeFirst())
    item_id = Field()


class RentalPropertyLoader(ItemLoader):
    default_item_class = RentalProperty
    default_output_processor = TakeFirst()
