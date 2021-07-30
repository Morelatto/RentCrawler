# RentCrawler

Crawlers para sites de aluguel com persistência de dados em banco não relacional e deduplicação de itens usando banco em memória. Os itens são enviados para um cluster Elasticsearch para serem analisados e visualizados no Kibana.

O projeto foi desenvolvido com o objetivo de agregar as informações disponíveis em vários sites de aluguel em um único local para facilitar a busca de um novo apartamento e ter mais parâmetros de busca além dos que os sites disponibilizam.

## Sites de aluguel

- [VivaReal](https://vivareal.com.br/)
- [ZAP Imóveis](https://www.zapimoveis.com.br/)
- [QuintoAndar](https://www.quintoandar.com.br/)

## Requisitos

- Python 3.8+
- Scrapy 2.5.0
- MongoDB
- Redis
- Elasticsearch

## Configurações

* rent_crawler/settings.py

```py
MONGODB_URI = 'mongodb://'
MONGODB_DATABASE = 'rent'
MONGODB_UNIQUE_KEY = 'code'
MONGODB_ADD_TIMESTAMP = True
MONGODB_SEPARATE_COLLECTIONS = True

ELASTICSEARCH_SERVERS = ['']
ELASTICSEARCH_INDEX = 'rent-items'
ELASTICSEARCH_UNIQ_KEY = 'code'
ELASTICSEARCH_BUFFER_LENGTH = 250

REDIS_HOST = ''
REDIS_PORT = 6379
```

## Parâmetros

- start_page
  - página inicial que o crawler vai realizar a extração
- pages_to_crawl
  - quantidade de páginas que o crawler deverá extrair 

Os crawlers usam as urls internas de cada site para extrair os dados ao invés de acessar a página de busca. Atualmente as urls estão apontando para a cidade de **São Paulo**, para atualizar o local é preciso descobrir essa url interna ou o payload de dados enviado na requisição de cada site para a cidade desejada e atualizar a variável _start_url_ ou o payload com esse valor. 

Mais informações em:
- https://docs.scrapy.org/en/latest/topics/developer-tools.html#the-network-tool
- https://docs.scrapy.org/en/latest/topics/dynamic-content.html

## Rodar local

Para rodar local e salvar os itens para um arquivo json sem enviar para nenhum banco ou cluster Elasticsearch, é preciso comentar a configuração dos pipelines no arquivo de configurações:

```py
ITEM_PIPELINES = {
    'rent_crawler.pipelines.RentCrawlerPipeline': 100,
    'rent_crawler.pipelines.RedisDuplicatePipeline': 200,
    'scrapy_mongodb.MongoDBPipeline': 300,
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 400
}
```

Instalar as dependências do projeto:

```
pip install -r requirements.txt
```


Rodar o crawler:

```
scrapy crawl vivareal -a start_page=1 -a pages_to_crawl=2 -o vivareal.json
```

# License

Distributed under the GNU License. See LICENSE for more information.