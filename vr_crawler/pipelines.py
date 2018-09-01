# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline

import logging
import scrapy
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class ApartmentPipeline:
    def __init__(self):
        self.db = r'apartments.sqlite'
        self.table = 'apartments'
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.__create_table()

    def process_item(self, item, _):
        self.__upsert(item)
        self.connection.commit()
        return item

    def __upsert(self, item):
        values = (item.get('name'), item.get('address').get('street'), item.get('address').get('district'),
                  item.get('address').get('city'), item.get('size'), item.get('rooms'), item.get('bathrooms'),
                  item.get('garages'), item.get('rent'), item.get('condo'), item.get('description'), item.get('code'))
        try:
            self.cursor.execute("INSERT INTO {} VALUES(?,?,?,?,?,?,?,?,?,?,?,?);".format(self.table), values)
        except sqlite3.IntegrityError:
            logger.debug('Updating item already on db: ' + item.get('code'))
            self.cursor.execute("UPDATE {} SET name = ?, street = ?, district = ?, city = ?, size = ?, rooms = ?, "
                                "bathrooms = ?, garages = ?, rent = ?, condo = ?, description = ? WHERE code = ?;"
                                .format(self.table), values)

    def __create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (name TEXT, street TEXT, district TEXT, city TEXT, "
                            "size INT, rooms INT, bathrooms INT, garages INT, rent INT, condo INT, description TEXT, "
                            "code INT PRIMARY KEY)".format(self.table))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class ApartmentPicturesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return '{}/{}.jpg'.format(request.meta['code'], request.meta['index'])

    def get_media_requests(self, item, info):
        for i, img_url in enumerate(item['img_urls']):
            meta = {'code': item['code'], 'index': i}
            yield scrapy.Request(url=img_url, meta=meta)
