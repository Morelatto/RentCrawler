from vr_crawler.items import AddressLoader, PricesLoader

import scrapy

CODES_FILE = 'codes.txt'
IMAGES_FOLDER = 'pictures'


class ApartmentPicturesSpider(scrapy.Spider):
    name = 'apartment_pictures'
    start_url = 'https://www.vivareal.com.br/busca-por-codigo/?id='

    custom_settings = {
        'ITEM_PIPELINES': {
            'vr_crawler.pipelines.ApartmentPicturesPipeline': 1
        },
        'IMAGES_STORE': IMAGES_FOLDER + '/'
    }

    def start_requests(self):
        with open(CODES_FILE) as codes_file:
            for code in codes_file:
                code = code.strip()
                yield scrapy.Request(url=self.start_url + code, headers={'Referer': 'https://www.vivareal.com.br'},
                                     meta={'code': code})

    def parse(self, response):
        img_urls = list()
        for img in response.css('.H .G img.hK'):
            data_src = img.xpath('@data-src')
            if data_src:
                img_urls.append(data_src.extract_first())
            else:
                img_urls.append(img.xpath('@src').extract_first())
        yield {
            'code': response.meta['code'],
            'img_urls': img_urls,
            'address': self.get_address(response),
            'prices': self.get_prices(response),
            'description': response.css('p.qm::text').extract_first(),
            'characteristics': response.css('.qn li::text').extract()
        }

    @classmethod
    def get_address(cls, response):
        address_loader = AddressLoader(selector=response)
        address_loader.add_css('street', 'a.B::text')
        address_loader.add_css('district', 'a.B::text')
        address_loader.add_css('city', 'a.B::text')
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, response):
        prices_loader = PricesLoader(selector=response)
        prices_loader.add_css('rent', '.js-detail-rent-price::text')
        prices_loader.add_css('condo', '.js-detail-condo-price::text')
        prices_loader.add_css('iptu', '.js-detail-iptu-price::text')
        return prices_loader.load_item()
