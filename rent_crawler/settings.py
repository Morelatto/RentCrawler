# -*- coding: utf-8 -*-

BOT_NAME = 'rent_crawler'

SPIDER_MODULES = ['rent_crawler.spiders']
NEWSPIDER_MODULE = 'rent_crawler.spiders'

USER_AGENT = \
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

# CONCURRENT_REQUESTS = 32

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True

DOWNLOAD_DELAY = 1

TELNETCONSOLE_ENABLED = False
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    'scrapy_mongodb.MongoDBPipeline': 300,
    'rent_crawler.pipelines.ApartmentPicturesPipeline': 1
}

MONGODB_DATABASE = 'rent'
MONGODB_COLLECTION = 'places'
MONGODB_UNIQUE_KEY = 'code'

# LOG_STDOUT = True
# LOG_FILE = 'spider_log.txt'

IMAGES_STORE = 'pictures/'

CLOSESPIDER_ITEMCOUNT = 100
