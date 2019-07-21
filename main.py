import re

import requests

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.spiders.vivareal import VivaRealSpider
from rent_crawler.spiders.zap import ZapSpider

vr_search_url = 'https://glue-api.vivareal.com/v1/locations'
zap_search_url = 'https://www.zapimoveis.com.br/busca/RetornarAutoSuggestLocalidadeImovel'
zap_friendly_url = 'https://www.zapimoveis.com.br/busca/ObterUrlAmigavelImovel'

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# TODO add logging on search results
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
    vr_r = requests.get(vr_search_url, params=vr_search_params, headers=headers)
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


def get_zap_crawl_params(query):
    zap_search_params = {
        'Utilizacao': 'imovel-geral',
        'termo': query,
        'quantidade': 15
    }
    zap_headers = {**{'X-Requested-With': 'XMLHttpRequest'}, **headers}
    zap_r = requests.get(zap_search_url, params=zap_search_params, headers=zap_headers)
    if zap_r.status_code == 200:
        response = zap_r.json()
        results = response.get('Resultados')
        if results and len(results):
            crits = results[0]['Criterios']
            zap_r = requests.post(zap_friendly_url, data=get_friendly_search_params(crits), headers=zap_headers)
            if zap_r.status_code == 200:
                friendly_url = zap_r.text
                zap_r = requests.get(friendly_url, headers=headers)
                if zap_r.status_code == 200:
                    seed_re = r'<input type="hidden" id="semente" data-value="(\d+)" />'
                    seed = re.findall(seed_re, zap_r.text)
                    if seed:
                        return {'seed': seed[0], 'friendly_url': friendly_url,
                                'parameters': get_parameters_auto_suggest(crits)}


def get_friendly_search_params(crits):
    zap_friendly_search_params = \
        '{{"Transacao":"Locacao",' \
        '"SubtipoImovel":"apartamento-padrao",' \
        '"ParametrosAutoSuggest":{},' \
        '"TipoOferta":"Imovel",' \
        '"PaginaOrigem":"Home",' \
        '"Pagina":1}}'.format(get_parameters_auto_suggest(crits))
    return {'parametrosBusca': zap_friendly_search_params, 'origem': 'Home'}


def get_parameters_auto_suggest(crits):
    return '[{{"Bairro":"{}","Cidade":"{}","Estado":"{}","Zona":"{}"}}]'.format(
        get_crit_value(crits, 'bairro'), get_crit_value(crits, 'cidade'),
        get_crit_value(crits, 'sigla'), get_crit_value(crits, 'zona'))


def get_crit_value(crits, name):
    for c in crits:
        n, v = c.split(':')
        if name == n:
            return v


def main():
    query = input('Enter search term: ')
    process = CrawlerProcess(get_project_settings())
    process.crawl(VivaRealSpider, **get_vr_crawl_params(query))
    process.crawl(ZapSpider, **get_zap_crawl_params(query))
    process.start()


if __name__ == '__main__':
    main()
