# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader, Selector
from itemloaders.processors import TakeFirst, Identity, MapCompose


def clear_str(input_str):
    return input_str.replace('\xa0', ' ')


def pack_properties(property_list):
    cleared_list = [clear_str(item) for item in property_list if len(item.strip()) > 0]
    property_dict = dict(zip([item for item in cleared_list[::2]],
                             [item for item in cleared_list[1::2]]))
    return property_dict


class Apartment(Item):
    title = Field()
    url = Field()
    price = Field()
    address = Field()
    seller_url = Field()
    properties = Field()


class ApartmentLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    properties_out = pack_properties
    title_in = MapCompose(clear_str)
