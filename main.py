from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.spiders.quintoandar import QuintoAndarSpider
from rent_crawler.spiders.vivareal import VivaRealSpider
from rent_crawler.spiders.zap import ZapSpider


def main():
    process = CrawlerProcess(get_project_settings())
    # process.crawl(VivaRealSpider)
    # process.crawl(ZapSpider)
    process.crawl(QuintoAndarSpider)
    process.start()


if __name__ == '__main__':
    main()
