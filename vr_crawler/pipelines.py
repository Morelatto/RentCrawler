# -*- coding: utf-8 -*-

import logging
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class ApartmentPipeline:
    def __init__(self):
        self.db = r'apartments3.sqlite'
        self.table = 'apartments'
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.__create_table()

    def process_item(self, item, _):
        self.__insert(item)
        self.connection.commit()
        return item

    def __insert(self, item):
        values = (item.get('name'), item.get('address').get('street'), item.get('address').get('district'),
                  item.get('address').get('city'), item.get('size'), item.get('rooms'), item.get('bathrooms'),
                  item.get('garages'), item.get('rent'), item.get('condo'), item.get('description'), item.get('code'))
        try:
            self.cursor.execute("INSERT INTO {table} VALUES(?,?,?,?,?,?,?,?,?,?,?,?);".format(table=self.table), values)
        except sqlite3.IntegrityError:
            logger.warning('Updating item already on db: ' + item.get('code'))
            self.cursor.execute('''UPDATE {table} SET 
            name = ?, 
            street = ?, 
            district = ?, 
            city = ?, 
            size = ?, 
            rooms = ?, 
            bathrooms = ?, 
            garages = ?, 
            rent = ?, 
            condo = ?, 
            description = ?
            WHERE code = ?;'''.format(table=self.table), values)

    def __create_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS {table}
            (name TEXT,
            street TEXT,
            district TEXT,
            city TEXT,
            size INT,
            rooms INT,
            bathrooms INT,
            garages INT,
            rent INT,
            condo INT,
            description TEXT,
            code INT PRIMARY KEY)
            '''.format(table=self.table))
        self.connection.commit()

    def handle_error(self, e):
        logger.error(e)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
