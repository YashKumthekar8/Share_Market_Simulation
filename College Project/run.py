from share_market.share_market.spiders.TCSScrap import QuoteSpider
import subprocess
from flask import Flask
from scrapy.crawler import CrawlerRunner

app = Flask('Share Market')
crawl_runner = CrawlerRunner()
data = []

if __name__ == '__main__':
    spider = QuoteSpider()
    print(spider.share_value_data)
    event = crawl_runner.crawl(QuoteSpider, data=data)
    print(data)