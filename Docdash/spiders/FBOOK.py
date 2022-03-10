import scrapy


class FbookSpider(scrapy.Spider):
    name = 'FBOOK'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def parse(self, response):
        pass
