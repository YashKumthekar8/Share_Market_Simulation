import re
import subprocess
import scrapy

class QuoteSpider(scrapy.Spider):

    name = "Wipro_shares"
    share_value_data = []
    time_line = []

    def start_requests(self):
        urls = ['https://moneybhai.moneycontrol.com/snapshot/stock-W.html']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def toString(self, string):
        regex = re.compile(r'[\n\r\t]')
        string = ' '.join(map(str, string))
        string = regex.sub("", string)
        return string

    def parse(self, response):
        details = {}

        share_value = response.css(".bold-number::text").extract()
        share_value = self.toString(share_value)
        details['share_value'] = share_value

        time_line = datetime.datetime.now()
        self.share_value_data.append(float(share_value))
        self.time_line.append(time_line.strftime('%H:%M:%S'))
        if len(self.share_value_data) > 100:
            self.share_value_data.pop(0)
            self.time_line.pop(0)

        increase_Points = response.css(".points::text").extract()
        increase_Points = self.toString(increase_Points)
        details['increasePoints'] = increase_Points
 
        percentage_increase = response.css(".percentage::text").extract()
        percentage_increase = self.toString(percentage_increase)
        details['percentage_increase'] = percentage_increase

        volume = response.css(".comp-vol strong::text").extract()
        volume = self.toString(volume)
        details['volume'] = volume

        market_cap = response.css(".key-info-list p::text").extract()
        market_cap = market_cap[1]
        details['market_cap'] = market_cap

        open_price = response.css(".comp-stat-item p::text").extract()
        open_price = open_price[2]
        details['open_price'] = open_price
        print(details)

        link = "https://www.moneycontrol.com/india/stockpricequote/computers-software/wipro/W"
        self.plotGraph()

    def plotGraph(self):
        plt.xkcd()

        self.share_value_data = [float(item) for item in self.share_value_data]

        print(self.share_value_data)
        try:
            plt.plot(self.time_line, self.share_value_data, color='k', linewidth=3,
                     marker='o', label='Share Value Trend')
        except ValueError:
            print('Value Error')
        plt.fill_between(self.share_value_data, y_values, facecolor='pink', interpolate=True)
        plt.ylabel('Share Value')
        plt.title('Share Value Trend Of TCS Company')
        plt.tight_layout()
        plt.grid(False)
        plt.savefig('plot.png')
        plt.show()
        

if __name__ == "__main__":
    subprocess.run("scrapy crawl Wipro_shares", shell=True)
