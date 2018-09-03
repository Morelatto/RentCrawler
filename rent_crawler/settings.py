# -*- coding: utf-8 -*-

BOT_NAME = 'rent_crawler'

SPIDER_MODULES = ['rent_crawler.spiders']
NEWSPIDER_MODULE = 'rent_crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

ROBOTSTXT_OBEY = False

# CONCURRENT_REQUESTS = 32

# DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {
    'rent_crawler.pipelines.ApartmentPipeline': 300,
    'rent_crawler.pipelines.ApartmentPicturesPipeline': 1
}

IMAGES_STORE = 'pictures/'

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# LOG_STDOUT = True
# LOG_FILE = 'spider_log.txt'
