import scrapy
import json
from scrapy.crawler import CrawlerProcess

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
        with open("./audio/product_crawl_data.json", "w") as file:
            file.truncate(0)

        # Extract clean text content from specific tags like <p>, <h1>, <h2>, etc.
        page_text = response.css('p::text').getall()  # Extract text from all <p> tags
        page_headings = response.css('h1::text, h2::text, h3::text').getall()  # Extract text from headings

        # Combine extracted text into one clean output
        clean_text = "\n".join(page_headings + page_text)

        # Yield the clean text
        yield {
            'url': response.url,
            'text': clean_text.strip(),  # Remove any leading/trailing spaces
        }

         # Create a dictionary with 'url' and 'text'
        page_data = {
            'url': response.url,
            'text': clean_text.strip(),
        }

        # Write the extracted data to a JSON file
        self.write_to_json(page_data)
        
        # Follow any links to continue scraping other pages
        next_pages = response.css('a::attr(href)').getall()
        for next_page in next_pages:
            if next_page and next_page.startswith("https://elevenlabs.io/"):
            # if next_page:
                yield response.follow(next_page, callback=self.parse)

    def write_to_json(self, data):
        # Open the output file in append mode
        with open("./audio/product_crawl_data.json", "a", encoding="utf-8") as f:
            # If the file is empty, write the opening square bracket to indicate a list
            if f.tell() == 0:
                f.write("[\n")
            else:
                f.write(",\n")
            
            # Write the JSON object
            json.dump(data, f, ensure_ascii=False, indent=4)

            # Check if it is the last entry, and close the array if necessary
            f.write("\n")

    def closed(self, reason):
        # Ensure that the JSON file ends with the closing bracket when the spider finishes
        with open("./audio/product_crawl_data.json", "a", encoding="utf-8") as f:
            f.write("\n]")



def crawl(context):
    # run scrapy crawl my_spider
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    process.join()
    with open("./audio/product_crawl_data.json", "r") as file:
        content = file.read()
        context['crawl_data'] = content

if __name__ == "__main__":
    context = {}
    crawl(context)
    # print(context['crawl_data'])
