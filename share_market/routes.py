import os
import io
import threading
from share_market import app, db
from share_market import Reliance_Company, TCS_Company, Infosys_Company, Wipro_Company, LandT_Company, HDFC_Company, SBI_Company, Zee_Media_Company, Ashok_Leyland_Company, Tech_Mahindra_Company
from flask import Flask, render_template, url_for, redirect, request
from share_market.models import Transaction, Portfolio, Data, Amount
from flask_sqlalchemy import SQLAlchemy
import subprocess
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import requests
import re
from flask import flash


page_name = None

@app.route("/")
@app.route("/Home")
def home():
    details = []
    company_names_url = ['RI', 'TCS', 'IT', 'W', 'LT', 'HDF01', 'SBI', 'ZN', 'AL', 'TM4']

    for i in range(0,10):
        url = f"https://moneybhai.moneycontrol.com/snapshot/stock-{company_names_url[i]}.html"
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        value = soup.find("p", class_="bold-number").get_text()
        value = toString(value)
        value = value.replace(" ", "")

        details.append(value)

        initialize()

    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/HDFC.png')
    image_file7 = url_for('static', filename='images/SBI.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('Home.html', title="Home", details=details, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


def initialize():
    if Amount.query.first() == None:
        amount = Amount(amount=float(10000000))
        print(amount)
        db.session.add(amount)
        db.session.commit()
    else:
        pass

def toString(string):
    regex = re.compile(r'[\n\r\t]')
    string = ' '.join(map(str, string))
    string = regex.sub("", string)
    return string


@app.route("/", methods=['GET', 'POST'])
def Search():
    if request.method == 'POST':
        search_term = request.form.get('srch-term')

    if search_term == "re":
        return redirect('/Reliance')
    elif search_term == "tcs":
        return redirect('/TCS')
    elif search_term == "in":
        return redirect('/Infosys')
    elif search_term == "wi":   
        return redirect('/Wipro')
    elif search_term == "l":
        return redirect('/L&T')
    elif search_term == "hd":
        return redirect('/HDFC')
    elif search_term == "sb":
        return redirect('/SBI')
    elif search_term == "zee":
        return redirect('/Zee')
    elif search_term == "as":
        return redirect('/Ashok_leyland')
    elif search_term == "te":
        return redirect('/Tech_Mahindra')


@app.route("/Reliance")
def Reliance():
    from matplotlib import pyplot as plt2
    plt2.switch_backend('agg')
    global page_name
    page_name = 'Reliance'
    plt2.xkcd()

    reliance = Reliance_Company.RelianceComp()
    reliance.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]
    print(min(time_line))
    print(max(time_line))
    value = Transaction.query.with_entities(Data.reliancesharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]
    
    try:
        plt2.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    
    plt2.ylabel('Share Value')
    plt2.title('Share Value Trend Of Reliance Company')
    plt2.tight_layout()
    plt2.grid(False)
    ax = plt2.gca()
    date = max(time_line)
    date += timedelta(days=1)
    date2 = min(time_line)
    date2 -= timedelta(days=1)
    ax.set_xlim([date2, date])
    ax.set_facecolor('xkcd:navy')
    plt2.xticks(rotation=60)

    # ax.axes.xaxis.set_ticks([])
    plt2.savefig('E:\Development\Flask Projects\Flask_College_Project\share_market\static\images\Reliancegraph.png', bbox_inches = "tight")
    image_file = url_for('static', filename='images/Reliancegraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('ReliancePage.html', details=reliance.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/TCS")
def TCS():
    from matplotlib import pyplot as plt
    plt.switch_backend('agg')
    global page_name
    page_name = 'TCS'
    plt.xkcd()

    tcs = TCS_Company.TCSComp()
    tcs.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.tcssharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]
    
    try:
        plt.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt.ylabel('Share Value')   
    plt.title('Share Value Trend Of TCS Company')
    plt.tight_layout()
    plt.grid(False)
    ax = plt.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])
    plt.savefig('E:\Development\Flask Projects\Flask_College_Project\share_market\static\images\TCSgraph.png')
    image_file = url_for('static', filename='images/TCSgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('TCSPage.html', details=tcs.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/Infosys")
def Infosys():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'Infosys'
    plt4.xkcd()

    infosys = Infosys_Company.InfosysComp()
    infosys.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.infosyssharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of Infosys Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('E:\Development\Flask Projects\Flask_College_Project\share_market\static\images\Infosysgraph.png')
    image_file = url_for('static', filename='images/Infosysgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('InfosysPage.html', details=infosys.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/Wipro")
def Wipro():
    from matplotlib import pyplot as plt3
    plt3.switch_backend('agg')
    global page_name
    page_name = 'Wipro'
    plt3.xkcd()

    wipro = Wipro_Company.WiproComp()
    wipro.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.wiprosharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt3.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
        
    plt3.ylabel('Share Value')
    plt3.title('Share Value Trend Of Wipro Company')
    plt3.tight_layout()
    plt3.grid(False)
    ax = plt3.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])
    plt3.savefig('E:\Development\Flask Projects\Flask_College_Project\share_market\static\images\Wiprograph.png')
    image_file = url_for('static', filename='images/Wiprograph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('WiproPage.html', details=wipro.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/L&T")
def LandT():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'L&T'
    plt4.xkcd()

    LandT = LandT_Company.LandTComp()
    LandT.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.landtsharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of L&T Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('E:\Development\Flask Projects\Flask_College_Project\share_market\static\images\L&Tgraph.png')
    image_file = url_for('static', filename='images/L&Tgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('L&TPage.html', details=LandT.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/HDFC")
def HDFC():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'HDFC'
    plt4.xkcd()

    HDFC = HDFC_Company.HDFCComp()
    HDFC.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.hdfcsharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of HDFC Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('D:\Python\Flask_College_Project\share_market\static\images\HDFCgraph.png')
    image_file = url_for('static', filename='images/HDFCgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('HDFCPage.html', details=HDFC.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)



@app.route("/SBI")
def SBI():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'SBI'
    plt4.xkcd()

    SBI = SBI_Company.SBIComp()
    SBI.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.sbisharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of SBI Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('D:\Python\Flask_College_Project\share_market\static\images\SBIgraph.png')
    image_file = url_for('static', filename='images/SBIgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('SBIPage.html', details=SBI.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/Zee Media")
def Zee_Media():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'Zee Media'
    plt4.xkcd()

    Zee_Media = Zee_Media_Company.Zee_MediaComp()
    Zee_Media.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.zeemediasharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of Zee Media Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('D:\Python\Flask_College_Project\share_market\static\images\Zee_Mediagraph.png')
    image_file = url_for('static', filename='images/Zee_Mediagraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('ZeeMediaPage.html', details=Zee_Media.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)



@app.route("/Ashok Leyland")
def Ashok_Leyland():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'Ashok Leyland'
    plt4.xkcd()

    Ashok_Leyland = Ashok_Leyland_Company.Ashok_LeylandComp()
    Ashok_Leyland.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.ashokleylandsharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of Ashok Leyland Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('D:\Python\Flask_College_Project\share_market\static\images\Ashok_Leylandgraph.png')
    image_file = url_for('static', filename='images/Ashok_Leylandgraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('AshokLeylandPage.html', details=Ashok_Leyland.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route("/Tech Mahindra")
def Tech_Mahindra():
    from matplotlib import pyplot as plt4
    plt4.switch_backend('agg')
    global page_name
    page_name = 'Tech Mahindra'
    plt4.xkcd()

    Tech_Mahindra = Tech_Mahindra_Company.Tech_MahindraComp()
    Tech_Mahindra.scrap_data()

    time_line = Transaction.query.with_entities(Data.timeline).all()
    time_line = list(time_line)
    time_line = [item for t in time_line for item in t]

    value = Transaction.query.with_entities(Data.techmahindrasharevalue).all()
    value = list(value)
    value = [item for t in value for item in t]

    try:
        plt4.plot(time_line, value, color='white', linewidth=1, label='Share Value Trend')
    except ValueError:
        print('Value Error')
    plt4.ylabel('Share Value')
    plt4.title('Share Value Trend Of Tech Mahindra Company')
    plt4.tight_layout()
    plt4.grid(False)
    ax = plt4.gca()
    ax.set_facecolor('xkcd:navy')
    ax.axes.xaxis.set_ticks([])   
    plt4.savefig('D:\Python\Flask_College_Project\share_market\static\images\Tech_Mahindragraph.png')
    image_file = url_for('static', filename='images/Tech_Mahindragraph.png')
    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/SBI.png')
    image_file7 = url_for('static', filename='images/HDFC.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('TechMahindraPage.html', details=Tech_Mahindra.details, image_file=image_file, image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, image_file9=image_file9, image_file10=image_file10)


@app.route(f'/Reliance', methods=['GET', 'POST'])
def buy_calcn():
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        price_now = float(request.form.get('current_price'))
        print(quantity)
        print(price_now)
        totalprice = float(quantity) * price_now
        
        transaction_1 = Transaction(companyname=page_name, typetransact='Buy', quantity=quantity, pricebought=price_now, totalprice=totalprice)

        db.session.add(transaction_1)
        db.session.commit()

        if Portfolio.query.filter_by(companyname=page_name).first() == None:
            pass
        else:
            portfolio = Portfolio.query.filter_by(companyname=page_name).first()
            quantity = quantity + portfolio.quantity
            totalprice = quantity * price_now
            db.session.delete(portfolio)
            db.session.commit()

        portfolio_1 = Portfolio(companyname=page_name, quantity=quantity, totalinvestment=totalprice)

        db.session.add(portfolio_1)
        db.session.commit()
        
        amount = Amount.query.all()
        amount = amount[0]
        obj = amount
        amount = getattr(amount, 'amount')
        amount_a = amount - quantity * price_now
        final_amount = Amount(amount=amount_a)
        db.session.delete(obj)
        db.session.commit()
        db.session.add(final_amount)
        db.session.commit()

    return redirect('/Portfolio')


@app.route(f'/TCS', methods=['GET', 'POST'])
def sell_calcn():
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        price_now = float(request.form.get('current_price'))

        totalprice = float(quantity) * price_now

        record = Portfolio.query.filter_by(companyname=page_name).first()
        
        if record == None:
            available_quantity = 0
        else:
            available_quantity = record.quantity

        if (available_quantity != 0) and (quantity <= available_quantity):
            transaction_1 = Transaction(companyname=page_name, typetransact='Sell', quantity=quantity, pricebought=price_now, totalprice=totalprice)

            db.session.add(transaction_1)
            db.session.commit()

            if Portfolio.query.filter_by(companyname=page_name).first() == None:
                pass
            else:
                portfolio = Portfolio.query.filter_by(companyname=page_name).first()
                quantity = portfolio.quantity - quantity
                totalprice = quantity * price_now
                db.session.delete(portfolio)
                db.session.commit()

            portfolio_1 = Portfolio(companyname=page_name, quantity=quantity, totalinvestment=totalprice)

            db.session.add(portfolio_1)
            db.session.commit()

            amount = Amount.query.all()
            amount = amount[0]
            obj = amount
            amount = getattr(amount, 'amount')
            amount_a = amount + quantity * price_now
            final_amount = Amount(amount=amount_a)
            db.session.delete(obj)
            db.session.commit()
            db.session.add(final_amount)
            db.session.commit()

            return redirect('/Portfolio')
        else:
            flash(f'Exceeded Available Quantities Present In Portfolio = {available_quantity}')
            print(page_name)
            return redirect(f'/{page_name}')


def transaction_details():
    transactions = Transaction.query.all()
    company_name = []
    date = []
    typetransact = []
    quantity = []
    pricebought = []
    totalprice = []
    rows = len(transactions)

    for i in range(rows):
        transaction = transactions[i]
        company_name.append(getattr(transaction, 'companyname'))
        date.append(getattr(transaction, 'date'))
        typetransact.append(getattr(transaction, 'typetransact'))
        quantity.append(getattr(transaction, 'quantity'))
        pricebought.append(getattr(transaction, 'pricebought'))
        totalprice.append(getattr(transaction, 'totalprice'))

    return company_name, date, typetransact, quantity, pricebought, totalprice, rows


def portfolio_details():
    portfolios = Portfolio.query.all()
    companyname = []
    quantity = []
    totalinvestment = []
    rows = len(portfolios)

    for i in range(rows):
        portfolio = portfolios[i]
        companyname.append(getattr(portfolio, 'companyname'))
        quantity.append(getattr(portfolio, 'quantity'))
        totalinvestment.append(getattr(portfolio, 'totalinvestment'))

    return companyname, quantity, totalinvestment, rows


@app.route("/Portfolio")
def Tran_Port():
    details = {}
    company_names_url = ['RI', 'TCS', 'IT', 'W', 'LT', 'HDF01', 'SBI', 'ZN', 'AL', 'TM4']
    company_name_list = ['Reliance', 'TCS', 'Infosys', 'Wipro', 'L&T', 'HDFC', 'SBI', 'Zee Media', 'Ashok Leyland', 'Tech Mahindra']

    for i in range(0,10):
        url = f"https://moneybhai.moneycontrol.com/snapshot/stock-{company_names_url[i]}.html"
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        value = soup.find("span", class_="percentage").get_text()
        details[company_name_list[i]] = value
    
    sorted_list = sorted(details, key=details.get)

    company_name, date, typetransact, quantity, pricebought, totalprice, t_rows = transaction_details()
    companyname, total_quantity, totalinvestment, p_rows = portfolio_details()

    total_amount = Amount.query.first()
    amount = total_amount.amount

    image_file1 = url_for('static', filename='images/reliance industries.png')
    image_file2 = url_for('static', filename='images/TCS.png')
    image_file3 = url_for('static', filename='images/Infosys.png')
    image_file4 = url_for('static', filename='images/wipro.jpg')
    image_file5 = url_for('static', filename='images/L&T.png')
    image_file6 = url_for('static', filename='images/HDFC.png')
    image_file7 = url_for('static', filename='images/SBI.png')
    image_file8 = url_for('static', filename='images/zee media.jpg')
    image_file9 = url_for('static', filename='images/ashok leyland.png')
    image_file10 = url_for('static', filename='images/tech mahindra.jpg')
    return render_template('Transaction.html', amount=amount, sorted_list=sorted_list, company_name=company_name, date=date, 
                            typetransact=typetransact, quantity=quantity, pricebought=pricebought, totalprice=totalprice, t_rows=t_rows, 
                            companyname=companyname, total_quantity=total_quantity, totalinvestment=totalinvestment, p_rows=p_rows, 
                            image_file1=image_file1, image_file2=image_file2, image_file3=image_file3, image_file4=image_file4, 
                            image_file5=image_file5, image_file6=image_file6, image_file7=image_file7, image_file8=image_file8, 
                            image_file9=image_file9, image_file10=image_file10)
