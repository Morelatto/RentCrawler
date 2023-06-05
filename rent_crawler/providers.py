from scrapy.http import Response
from scrapy_poet.page_input_providers import PageObjectInputProvider


class BodyJson(dict): pass


class BodyJsonProvider(PageObjectInputProvider):
    provided_classes = {BodyJson}

    def __call__(self, to_provide, response: Response):
        return [BodyJson(response.json())]
