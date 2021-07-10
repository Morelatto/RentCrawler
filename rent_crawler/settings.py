# -*- coding: utf-8 -*-
BOT_NAME = 'rent_crawler'

SPIDER_MODULES = ['rent_crawler.spiders']
NEWSPIDER_MODULE = 'rent_crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 ' \
             'Safari/601.3.9 '

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
    'rent_crawler.pipelines.AwsDynamoDbPipeline': 300,
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 400
}

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
DYNAMODB_PIPELINE_REGION_NAME = 'sa-east-1'

ELASTICSEARCH_SERVERS = ['']
ELASTICSEARCH_INDEX = 'rent_crawler'
ELASTICSEARCH_INDEX_DATE_FORMAT = '%d/%m/%Y'
ELASTICSEARCH_TYPE = 'rent_properties'
ELASTICSEARCH_UNIQ_KEY = 'item-id'  # Custom unique key

REDIS_HOST = ''
REDIS_PORT = 6379

# LOG_STDOUT = True
# LOG_FILE = 'spider_log.txt'

# HTTPERROR_ALLOW_ALL = True
