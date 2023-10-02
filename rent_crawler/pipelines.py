# -*- coding: utf-8 -*-
import datetime
import logging

from pymongo.mongo_client import MongoClient
from pymongo.read_preferences import ReadPreference
from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy_redis import connection
from twisted.internet.threads import deferToThread

default_serialize = ScrapyJSONEncoder().encode


class RentItemPipeline:

    def __init__(self, database, collection, unique_key, stats, server, key, **kwargs):
        super(RentItemPipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger("scrapy-pipeline")
        self.database = database
        self.collection = collection
        self.unique_key = unique_key
        self.stats = stats
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings, spider_name, stats):
        db_connection = MongoClient(settings["MONGODB_URI"], read_preference=ReadPreference.PRIMARY)
        database = db_connection[settings["MONGODB_DATABASE"]]
        params = {
            'database': database,
            'collection': database[spider_name],
            'unique_key': settings["MONGODB_UNIQUE_KEY"],
            'stats': stats,
            'server': connection.from_settings(settings),
            'key': f'{spider_name}:start_urls'
        }

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings, crawler.spider.name, crawler.stats)

    def process_item(self, item, spider):
        if self.unique_key in item:
            process_method = self._process_item
        else:
            process_method = self._process_page_item
        return deferToThread(process_method, item, spider)

    def _process_item(self, item, spider):
        try:
            for k, v in item.items():
                if v is None or v == "":
                    spider.logger.warning(f'Null field: {k} in item: {item}')
        except Exception as ex:
            spider.logger.warning(f"Error {ex}")

        try:
            item = dict(item)
            item["scrapped_at"] = datetime.datetime.utcnow()
        except TypeError:
            spider.logger.warning(f"Failed to serialize item: {item}")

        try:
            key = {self.unique_key: item[self.unique_key]}
            self.collection.update_one(key, {'$set': item}, upsert=True)
            self.logger.debug("Stored item in MongoDB")
            self.stats.inc_value('mongodb/items_saved')
        except Exception as e:
            self.logger.error(f"Error while saving item: {str(e)}")
            self.stats.inc_value('mongodb/save_errors')
            raise DropItem(f"Error while saving item: {str(e)}")

        return item

    def _process_page_item(self, item, spider):
        data = default_serialize(item)
        self.server.rpush(self.key, data)
        self.stats.inc_value('redis/items_saved')
        return item
