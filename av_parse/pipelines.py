# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from itemadapter import ItemAdapter
from .items import Apartment
from .settings import BOT_NAME
import av_parse.settings as settings


class AvParsePipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client[BOT_NAME]
        self.collections = {
            Apartment.__name__: settings.MONGO_COLLECTION_APARTMENTS,
        }

    def process_item(self, item, spider):
        self.db[self.collections[item.__class__.__name__]].insert_one(ItemAdapter(item).asdict())
        return item
