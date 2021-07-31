# -*- coding: utf-8 -*-
BOT_NAME = 'rent_crawler'

SPIDER_MODULES = ['rent_crawler.spiders']
NEWSPIDER_MODULE = 'rent_crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 ' \
             'Safari/601.3.9'

DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 30

CONCURRENT_REQUESTS_PER_DOMAIN = 1

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_DEBUG = True

COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {
    'rent_crawler.pipelines.RentCrawlerPipeline': 100,
    'rent_crawler.pipelines.RedisDuplicatePipeline': 200,
    'scrapy_mongodb.MongoDBPipeline': 300,
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 400
}

MONGODB_URI = ''
MONGODB_DATABASE = 'rent'
MONGODB_UNIQUE_KEY = 'code'
MONGODB_ADD_TIMESTAMP = True
MONGODB_SEPARATE_COLLECTIONS = True

ELASTICSEARCH_SERVERS = ['']
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = 'code'
ELASTICSEARCH_BUFFER_LENGTH = 250

REDIS_HOST = ''
REDIS_PORT = 6379

# LOG_STDOUT = True
# LOG_FILE = 'spider_log.txt'
LOG_FORMATTER = 'rent_crawler.loggers.QuietLogFormatter'

# HTTPERROR_ALLOW_ALL = True
