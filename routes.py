from share_market import app
from share_market import Reliance_Company, TCS_Company, Wipro_Company, Infosys_Company

@app.route("/")
def home():
    return "Hello, Welcome TO Share Market"

@app.route("/TCS")
def TCS():
    TCS_Company.timerPrint()
    return "Welcome to TCS"

@app.route("/Reliance")
def Reliance():
    Reliance_Company.timerPrint()
    return "Welcome to Reliance"


@app.route("/Wipro")
def Wipro():
    Wipro_Company.timerPrint()
    return "Welcome to Wipro"


@app.route("/Infosys")
def Infosys():
    Infosys_Company.timerPrint()
    return "Welcome to Infosys"
