import scrapy
from scraper.items import OnisrItem

class OnisrItemSpider(scrapy.Spider):
    name = 'onisr'
    allowed_domains = ['onisr.securite-routiere.gouv.fr']
    start_urls = ['https://www.onisr.securite-routiere.gouv.fr/']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = set()

    def parse(self, response):
        print("Visiting:", response.url)
        item = OnisrItem()
        item['title'] = response.css('title::text').get()
        item['subtitles'] = response.css('h2::text').getall()
        item['paragraphs'] = response.css('p::text').getall()
        yield item
        
        for href in response.css('a::attr(href)').extract():
            if 'mailto:' in href or 'tel:' in href:
                continue
            url = response.urljoin(href)
            if url.lower().endswith('.pdf'):
                continue
            if (
                self.allowed_domains[0] in url and
                url not in self.visited_urls and
                '/en' not in url and '/es' not in url
            ):
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse)