import json

from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess

from seed import save_data


class Pipeline:
    authors = []
    quotes = []
    
    def process_item(self, item, spider):
        if "quote" in item.keys():
            self.quotes.append(item)
        if "fullname" in item.keys():
            self.authors.append(item)
            
    def close_spider(self, spider):    
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, indent=4, ensure_ascii=False)
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, indent=4, ensure_ascii=False)
        save_data()
    


class QuoteSpider(Spider):
    name = "get_quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"ITEM_PIPELINES":{Pipeline:200}}
    
    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='quote']"):
            tags = q.xpath("div[@class='tags']/a/text()").extract()
            quote:str = q.xpath("span[@class='text']/text()").get()
            author:str = q.xpath("span/small[@class='author']/text()").get()
            tags = [tag.strip() for tag in tags]
            yield {'tags': tags, 'quote':quote.strip(), 'author':author.strip()}
            yield response.follow(url=self.start_urls[0] + q.xpath("span/a/@href").get(), callback=self.parse_author)
        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield Request(url=self.start_urls[0] + next_link)

            
    def parse_author(self, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname": content.xpath("h3[@class='author-title']/text()").get().strip(),
            "born_date": content.xpath("p/span[@class='author-born-date']/text()").get().strip(),
            "born_location":content.xpath("p/span[@class='author-born-location']/text()").get().strip(),
            "description": content.xpath("div[@class='author-description']/text()").get().strip(),
        }
        
        
if __name__=="__main__":
    process = CrawlerProcess()
    process.crawl(QuoteSpider)
    process.start()
