# -*- coding: utf-8 -*-
BOT_NAME = "rent_crawler"

SPIDER_MODULES = ["rent_crawler.spiders"]
NEWSPIDER_MODULE = "rent_crawler.spiders"

DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 16

CONCURRENT_REQUESTS_PER_DOMAIN = 1

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_DEBUG = True

COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    'scrapy_poet.InjectionMiddleware': 543,
}

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",
    "scrapy_fake_useragent.providers.FakerProvider",
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 "
    "Safari/601.3.9"
)

ITEM_PIPELINES = {
    "rent_crawler.pipelines.RentCrawlerPipeline": 100,
    "rent_crawler.pipelines.RedisDuplicatePipeline": 200,
    "rent_crawler.pipelines.MongoDBPipeline": 300,
    "rent_crawler.pipelines.RedisPipeline": 400,
}

MONGODB_URI = 'mongodb://root:pass@localhost:27017'
MONGODB_DATABASE = 'rent'
MONGODB_UNIQUE_KEY = 'code'
MONGODB_ADD_TIMESTAMP = True
MONGODB_SEPARATE_COLLECTIONS = True

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB_NUMBER = 0

# LOG_STDOUT = True
# LOG_FILE = 'spider_log.txt'
LOG_FORMATTER = "rent_crawler.loggers.QuietLogFormatter"

# HTTPERROR_ALLOW_ALL = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

SCRAPY_POET_PROVIDERS = {
    "rent_crawler.providers.BodyJsonProvider": 500,
}

FEED_EXPORT_ENCODING = 'utf-8'
