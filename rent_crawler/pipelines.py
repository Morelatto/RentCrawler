# -*- coding: utf-8 -*-
import datetime
import logging

from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.read_preferences import ReadPreference

from scrapy.exporters import BaseItemExporter


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
            if self.settings[setting]:
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

        try:
            for k, v in item.items():
                if v is None or v == "":
                    spider.logger.warning(f'Null field: {k} in item: {item}')
        except Exception as ex:
            # log or print the problematic item here, e.g.
            spider.logger.warning(f"Error {ex}")

        try:
            item = dict(self._get_serialized_fields(item))
            # continue with your pipeline
        except TypeError:
            # log or print the problematic item here, e.g.
            spider.logger.warning(f"Failed to serialize item: {item}")

        item = {k: v for k, v in item.items() if v is not None and v != ""}

        expanded_item = {}
        for k, v in item.items():
            if v is not None and v != "":
                expanded_item[k] = v
            else:
                spider.logger.warning(f'Null field: {k} in item: {item}')

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
