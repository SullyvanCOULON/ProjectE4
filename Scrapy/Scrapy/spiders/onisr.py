import scrapy
from Scrapy.items import OnisrItem

class OnisrItemSpider(scrapy.Spider):
    name = 'onisr'
    allowed_domains = ['onisr.securite-routiere.gouv.fr']
    start_urls = ['https://www.onisr.securite-routiere.gouv.fr/']
    
    def parse(self, response):
        item = OnisrItem()
        item['title'] = response.css('title::text').get()
        item['subtitles'] = response.css('h2::text').getall()
        item['paragraphs'] = response.css('p::text').getall()[:5]
        yield item