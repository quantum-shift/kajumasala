import scrapy

class MySpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ["https://elevenlabs.io/docs/overview"]

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 50,
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            }
        }
    }

    def parse(self, response):
        page_text = response.css('*::text').getall()

        yield {
            'url': response.url,
            'text': page_text,
        }

        next_pages = response.css('a::attr(href)').getall()
        for next_page in next_pages:
            if next_page:
                yield response.follow(next_page, callback=self.parse)
        