import os
import io
import threading
from share_market import app, db
from share_market import TCS_Company, Reliance_Company, Wipro_Company, Infosys_Company
from flask import Flask, render_template, url_for, redirect, request
from share_market.models import Transaction, Portfolio, Data, Amount
from flask_sqlalchemy import SQLAlchemy
import subprocess
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import re

def timer(threadName):
    lock.acquire()
    time_start = 9
    time_end = 17
    while True:
        time_now = datetime.now().hour
        if time_start <= time_now < time_end:
            scrapping_data()
        time.sleep(600)
    lock.release()


def scrapping_data():
    url = "https://moneybhai.moneycontrol.com/snapshot/stock-W.html"

    company_names_url = ['TCS', 'RI', 'IT', 'W', 'SBI', 'HDF01', 'LT', 'ZN', 'TM4', 'AL']
    shares = []

    for i in range(0,10):
        url = f"https://moneybhai.moneycontrol.com/snapshot/stock-{company_names_url[i]}.html"
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        value = soup.find("p", class_="bold-number").get_text()
        value = toString(value)
        value = value.replace(" ", "")
        shares.append(value)

    data = Data(tcssharevalue=shares[0], reliancesharevalue=shares[1], infosyssharevalue=shares[2], wiprosharevalue=shares[3], sbisharevalue=shares[4], hdfcsharevalue=shares[5], landtsharevalue=shares[6], zeemediasharevalue=shares[7], techmahindrasharevalue=shares[8], ashokleylandsharevalue=shares[9])
    db.session.add(data)
    db.session.commit()


def toString(string):
    regex = re.compile(r'[\n\r\t]')
    string = ' '.join(map(str, string))
    string = regex.sub("", string)
    return string


if __name__ == "__main__":
    lock = threading.Lock()
    threading._start_new_thread(timer , ('Thread1', ))
    app.run(debug=True)