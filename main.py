import requests

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.spiders.vivareal import VivaRealSpider
from rent_crawler.spiders.zap import ZapSpider

vr_search_url = 'https://glue-api.vivareal.com/v1/locations'


def get_vr_crawl_params(query):
    vr_search_params = {
        'q': query,
        'fields': 'suggest',
        'filter': 'filter.pricingInfo.businessType:"RENTAL" AND '
                  'filter.listingType:"USED" AND '
                  'filter.unitType IN ["APARTMENT"]',
        'includeFields': 'city,neighborhood,street',
        'size': 6
    }
    vr_r = requests.get(vr_search_url, params=vr_search_params)
    if vr_r.status_code == 200:
        response = vr_r.json()
        max_score = {'maxScore': 0, 'result': {'locations': []}}
        for k in response:
            v = response[k]
            if v.get('maxScore', 0) > max_score['maxScore']:
                max_score = v
        locations = (max_score['result']['locations'])
        if len(locations):
            return {'location_id': locations[0]['address']['locationId']}


def main():
    query = input('Enter search term: ')
    process = CrawlerProcess(get_project_settings())
    process.crawl(VivaRealSpider, **get_vr_crawl_params(query))
    # TODO receive args in zap spider
    # process.crawl(ZapSpider)
    process.start()


if __name__ == '__main__':
    main()
