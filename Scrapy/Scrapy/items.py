import scrapy

class OnisrItem(scrapy.Item):
    title = scrapy.Field()
    subtitles = scrapy.Field()
    paragraphs = scrapy.Field()
