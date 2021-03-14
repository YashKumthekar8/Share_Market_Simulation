import scrapy
import subprocess


class QuoteSpider(scrapy.Spider):

    name = 'shares'

    def start_requests(self):
        urls = ['https://moneybhai.moneycontrol.com/myspace']
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = []

        # quotes = response.css("article div.stkvalue#ind_glb_currvalue1").extract()
        sensexValue = response.css(".sensxNumb::text").extract()
        sensexPer = response.css(".sensxplval::text").extract()
        # niftyValue = response.css()
        sensex_value = sensexValue[0]
        sensex_per = sensexPer[0]
        nifty_value = sensexValue[1]
        nifty_per = sensexPer[1]
        print(sensex_value)
        print(sensex_per)
        print(nifty_value)
        print(nifty_per)


if __name__ == "__main__":
    subprocess.run("scrapy crawl shares", shell=True)
