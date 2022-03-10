import scrapy


class LeadsrainRvmSpider(scrapy.Spider):
    name = 'LEADSRAIN_RVM'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def parse(self, response):
        pass
