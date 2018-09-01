import scrapy

CODES_FILE = 'codes.txt'
IMAGES_FOLDER = 'pictures/'


class ApartmentPicturesSpider(scrapy.Spider):
    name = 'apartment_pictures'
    start_url = 'https://www.vivareal.com.br/busca-por-codigo/?id='
    custom_settings = {
        'ITEM_PIPELINES': {
            'vr_crawler.pipelines.ApartmentPicturesPipeline': 1
        },
        'IMAGES_STORE': IMAGES_FOLDER
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
        yield {'code': response.meta['code'], 'img_urls': img_urls}
