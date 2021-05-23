from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.spiders.vivareal import VivaRealSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(VivaRealSpider)
    # process.crawl(ZapSpider, **get_zap_crawl_params(query))
    process.start()


if __name__ == '__main__':
    main()
