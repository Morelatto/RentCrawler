# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import logging

import redis
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.read_preferences import ReadPreference

from scrapy.exporters import BaseItemExporter

ITEM_ID_KEY = "item_id"


class RentCrawlerPipeline:
    def process_item(self, item, spider):
        item_hash = hashlib.sha1()
        item_dict = ItemAdapter(item).asdict()
        item_json = json.dumps(item_dict, sort_keys=True)
        item_hash.update(item_json.encode("utf-8"))
        item[ITEM_ID_KEY] = item_hash.hexdigest()
        return item


redis_key_prefix = {
    "vivareal": "VR",
    "zap": "ZAP",
    "quintoandar": "QUINTO",
}


class RedisDuplicatePipeline:
    def __init__(self, redis_host, redis_port, redis_db_number):
        if redis_host is not None:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db_number)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        redis_host = settings.get("REDIS_HOST")
        redis_port = settings.get("REDIS_PORT", default=6379)
        redis_db_number = settings.get("REDIS_DB_NUMBER", default=0)
        return cls(redis_host, redis_port, redis_db_number)

    def process_item(self, item, spider):
        if self.redis_client is None:
            return item

        if ITEM_ID_KEY in item:
            redis_id = f"{redis_key_prefix[spider.name]}:{item[ITEM_ID_KEY]}"
            existing_id = self.redis_client.get(redis_id)
            if existing_id is not None:
                raise DropItem("Duplicate item found")

        return item


class RedisPipeline(object):
    def __init__(self, redis_host, redis_port):
        if redis_host is not None:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        redis_host = settings.get("REDIS_HOST")
        redis_port = settings.get("REDIS_PORT", default=6379)
        return cls(redis_host, redis_port)

    def process_item(self, item, spider):
        if ITEM_ID_KEY in item:
            redis_id = f"{redis_key_prefix[spider.name]}:{item[ITEM_ID_KEY]}"
            self.redis_client.set(redis_id, "SEEN")
        return item


def not_set(string):
    """Check if a string is None or ''.

    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == "":
        return True
    return False


class MongoDBPipeline(BaseItemExporter):
    """MongoDB pipeline."""

    # Default options
    config = {
        "uri": "mongodb://localhost:27017",
        "fsync": False,
        "write_concern": 0,
        "database": "scrapy-mongodb",
        "collection": "items",
        "separate_collections": False,
        "replica_set": None,
        "unique_key": None,
        "buffer": None,
        "append_timestamp": False,
        "stop_on_duplicate": 0,
    }

    # Item buffer
    current_item = 0
    item_buffer = []

    # Duplicate key occurence count
    duplicate_key_count = 0

    def __init__(self, **kwargs):
        """Constructor."""
        super(MongoDBPipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger("scrapy-mongodb-pipeline")

    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

        # Versions prior to 0.25
        if not hasattr(spider, "update_settings") and hasattr(
                spider, "custom_settings"
        ):
            self.settings.setdict(spider.custom_settings or {}, priority="project")

    def open_spider(self, spider):
        self.load_spider(spider)

        # Configure the connection
        self.configure()

        # For a replica set, MongoDB connection string URI should contain all the hosts
        if self.config["replica_set"] is not None:
            connection_uri = (
                    self.config["uri"]
                    + "/?replicaSet="
                    + self.config["replica_set"]
                    + "&w="
                    + str(self.config["write_concern"])
                    + "&fsync="
                    + str(self.config["fsync"]).lower()
            )
            connection = MongoClient(
                connection_uri, read_preference=ReadPreference.PRIMARY_PREFERRED
            )
        else:
            # Connecting to a stand alone MongoDB
            connection_uri = (
                    self.config["uri"] + "/?fsync=" + str(self.config["fsync"]).lower()
            )
            connection = MongoClient(
                connection_uri, read_preference=ReadPreference.PRIMARY
            )

        # Set up the database
        self.database = connection[self.config["database"]]
        self.collections = {"default": self.database[self.config["collection"]]}

        self.logger.info(
            'Connected to MongoDB {0}, using "{1}"'.format(
                self.config["uri"], self.config["database"]
            )
        )

        # Get the duplicate on key option
        if self.config["stop_on_duplicate"]:
            tmpValue = self.config["stop_on_duplicate"]

            if tmpValue < 0:
                msg = (
                    "Negative values are not allowed for"
                    " MONGODB_STOP_ON_DUPLICATE option."
                )

                self.logger.error(msg)
                raise SyntaxError(msg)

            self.stop_on_duplicate = self.config["stop_on_duplicate"]

        else:
            self.stop_on_duplicate = 0

    def configure(self):
        """Configure the MongoDB connection."""
        # Handle deprecated configuration
        if not not_set(self.settings["MONGODB_HOST"]):
            self.logger.warning("DeprecationWarning: MONGODB_HOST is deprecated")
            mongodb_host = self.settings["MONGODB_HOST"]

            if not not_set(self.settings["MONGODB_PORT"]):
                self.logger.warning("DeprecationWarning: MONGODB_PORT is deprecated")
                self.config["uri"] = "mongodb://{0}:{1:i}".format(
                    mongodb_host, self.settings["MONGODB_PORT"]
                )
            else:
                self.config["uri"] = "mongodb://{0}:27017".format(mongodb_host)

        # Set all regular options
        options = [
            ("uri", "MONGODB_URI"),
            ("fsync", "MONGODB_FSYNC"),
            ("write_concern", "MONGODB_REPLICA_SET_W"),
            ("database", "MONGODB_DATABASE"),
            ("collection", "MONGODB_COLLECTION"),
            ("separate_collections", "MONGODB_SEPARATE_COLLECTIONS"),
            ("replica_set", "MONGODB_REPLICA_SET"),
            ("unique_key", "MONGODB_UNIQUE_KEY"),
            ("buffer", "MONGODB_BUFFER_DATA"),
            ("append_timestamp", "MONGODB_ADD_TIMESTAMP"),
            ("stop_on_duplicate", "MONGODB_STOP_ON_DUPLICATE"),
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        # Check for illegal configuration
        if self.config["buffer"] and self.config["unique_key"]:
            msg = (
                "IllegalConfig: Settings both MONGODB_BUFFER_DATA "
                "and MONGODB_UNIQUE_KEY is not supported"
            )
            self.logger.error(msg)
            raise SyntaxError(msg)

    def process_item(self, item, spider):
        """Process the item and add it to MongoDB.

        :type item: Item object
        :param item: The item to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        item = dict(self._get_serialized_fields(item))

        item = {k: v for k, v in item.items() if v is not None and v != ""}

        if self.config["buffer"]:
            self.current_item += 1

            if self.config["append_timestamp"]:
                item["scrapped_at"] = datetime.datetime.utcnow()

            self.item_buffer.append(item)

            if self.current_item == self.config["buffer"]:
                self.current_item = 0

                try:
                    return self.insert_item(self.item_buffer, spider)
                finally:
                    self.item_buffer = []

            return item

        return self.insert_item(item, spider)

    def close_spider(self, spider):
        """Be called when the spider is closed.

        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: None
        """
        if self.item_buffer:
            self.insert_item(self.item_buffer, spider)

    def insert_item(self, item, spider):
        """Process the item and add it to MongoDB.

        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        if not isinstance(item, list):
            item = dict(item)

            if self.config["append_timestamp"]:
                item["scrapped_at"] = datetime.datetime.utcnow()

        collection_name, collection = self.get_collection(spider.name)

        if self.config["unique_key"] is None:
            try:
                collection.insert_one(item)
                self.logger.debug(
                    "Stored item(s) in MongoDB {0}/{1}".format(
                        self.config["database"], collection_name
                    )
                )

            except errors.DuplicateKeyError:
                self.logger.debug("Duplicate key found")
                if self.stop_on_duplicate > 0:
                    self.duplicate_key_count += 1
                    if self.duplicate_key_count >= self.stop_on_duplicate:
                        self.crawler.engine.close_spider(
                            spider, "Number of duplicate key insertion exceeded"
                        )

        else:
            key = {}

            if isinstance(self.config["unique_key"], list):
                for k in dict(self.config["unique_key"]).keys():
                    key[k] = item[k]
            else:
                key[self.config["unique_key"]] = item[self.config["unique_key"]]

            collection.update_one(key, {'$set': item}, upsert=True)

            self.logger.debug(
                u'Stored item(s) in MongoDB {0}/{1}'.format(
                    self.config['database'], self.config['collection'])
            )

        return item

    def get_collection(self, name):
        if self.config["separate_collections"]:
            collection = self.collections.get(name)
            collection_name = name

            if collection is None:
                collection = self.database[name]
                self.collections[name] = collection
        else:
            collection = self.collections.get("default")
            collection_name = self.config["collection"]

        # Ensure unique index
        if self.config["unique_key"]:
            collection.create_index(self.config["unique_key"], unique=True)

        return (collection_name, collection)
