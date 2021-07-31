from setuptools import setup, find_packages

setup(
    name='RentCrawler',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = rent_crawler.settings']},
    install_requires=['scrapy-mongodb==0.12.0', 'redis==3.5.3', 'ScrapyElasticSearch==0.9.2']
)
