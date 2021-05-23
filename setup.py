from setuptools import setup, find_packages

setup(
    name='RentCrawler',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = rent_crawler.settings']},
    install_requires=['scrapy_dynamodb==0.2.3']
)
