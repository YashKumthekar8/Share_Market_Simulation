from flask import Flask
from bs4 import BeautifulSoup
import requests
import datetime
import re
from matplotlib import pyplot as plt
import threading
import time
import datetime


class HDFCComp():

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

        link = 'https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/hdfcbank/HDF01'
        self.details['link'] = link

    
def main():
    pass

if __name__ == "__main__":
    main()
