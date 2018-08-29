# -*- coding: utf-8 -*-

import logging
import sqlite3


class ApartmentPipeline:
    def __init__(self):
        self.db = r'apartments.sqlite'
        self.table = 'apartments'
        self.buff = list()
        self.buff_size = 20
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        self.cur.execute(
            '''
            create table if not exists {table}
            (name TEXT,
            address TEXT,
            size INT,
            rooms INT,
            bathrooms INT,
            garages INT,
            rent INT,
            condo INT,
            description TEXT,
            code INT PRIMARY KEY)
            '''.format(table=self.table))

    def __del__(self):
        if len(self.buff) > 0:
            self.__insert()
            self.con.commit()
        self.cur.close()
        self.con.close()

    def process_item(self, item, spider):
        self.buff.append((
            item['name'], item['address'], item['size'], item.get('rooms', 0), item.get('bathrooms', 0),
            item.get('garages', 0), item['rent'], item.get('condo', 0), item['description'], item['code']))
        if len(self.buff) == self.buff_size:
            self.__insert()
            self.con.commit()
            del self.buff[:]
        return item

    def __insert(self):
        try:
            self.cur.executemany("INSERT INTO {table} VALUES(?,?,?,?,?,?,?,?,?,?);".format(table=self.table), self.buff)
        except sqlite3.IntegrityError:
            logging.warning('Skipping item already on db')
