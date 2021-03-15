from flask import Flask
from bs4 import BeautifulSoup
import requests
import datetime
import re
from matplotlib import pyplot as plt
import threading
import time
import datetime


class Reliance():

    share_value = []
    details = {}
    time_line = []


    def toString(self, string):
        regex = re.compile(r'[\n\r\t]')
        string = ' '.join(map(str, string))
        string = regex.sub("", string)
        return string


    def scrap_data(self):
        url = "https://moneybhai.moneycontrol.com/snapshot/stock-RI.html"
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        value = soup.find("p", class_="bold-number").get_text()
        value = self.toString(value)
        value = value.replace(" ", "")
        self.details['share_value'] = value
        self.share_value.append(float(value))

        time = datetime.datetime.now()
        self.time_line.append(time.strftime('%H:%M:%S'))

        increase_points = soup.find("p", class_="points").get_text()
        self.details['increasePoints'] = increase_points

        percentage_increase = soup.find("span", class_="percentage").get_text()
        self.details['percentage_increase'] = percentage_increase

        p = soup.find("p", class_="comp-vol")
        volume = p.find("strong").get_text()
        self.details['volume'] = volume

        ul = soup.find("ul", class_="key-info-list")
        li = ul.find("li")
        market_cap = li.select('li > p')[1].get_text(strip=True)
        self.details['market_cap'] = market_cap

        div = soup.find("div", class_="comp-stat-item")
        open_price = div.select('div > p')[1].get_text(strip=True)
        self.details['open_price'] = open_price

        print(self.details)
        print(self.share_value)

        link = 'https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI'
        self.plotGraph()


    def plotGraph(self):
        plt.xkcd()

        self.share_value = [float(item) for item in self.share_value]

        try:
            plt.plot(self.time_line, self.share_value, color='k', linewidth=3,
                    marker='o', label='Share Value Trend')
        except ValueError:
            print('Value Error')
        plt.fill_between(self.time_line, self.share_value, facecolor='pink', interpolate=True)
        plt.ylabel('Share Value')
        plt.title('Share Value Trend Of Reliance Company')
        plt.tight_layout()
        plt.grid(False)
        plt.savefig('plot.png')
        plt.show()

def timerPrint():
    reliance = Reliance()
    now_time = datetime.datetime.now()
    tim = now_time.hour
    mins = now_time.minute
    while tim != 17 and mins != 31:
        reliance.scrap_data()
        time.sleep(120)


timerPrint()


