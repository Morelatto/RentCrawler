# -*- coding: utf-8 -*-
import logging

from scrapy_dynamodb import DynamoDbPipeline

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)


class AwsDynamoDbPipeline(DynamoDbPipeline):
    pass
