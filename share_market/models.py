from datetime import datetime
from share_market import db, app


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    typetransact = db.Column(db.String(5), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    pricebought = db.Column(db.Float, nullable=False)
    totalprice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Transaction('{self.companyname}', '{self.date}', {self.typetransact}', '{self.quantity}, '{self.pricebought}', '{self.totalprice}')"


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    totalinvestment = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Portfolio('{self.companyname}', '{self.quantity}', '{self.totalinvestment}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeline = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tcssharevalue = db.Column(db.Float, nullable=False)
    reliancesharevalue = db.Column(db.Float, nullable=False)
    infosyssharevalue = db.Column(db.Float, nullable=False)
    wiprosharevalue = db.Column(db.Float, nullable=False)
    sbisharevalue = db.Column(db.Float, nullable=False)
    hdfcsharevalue = db.Column(db.Float, nullable=False)
    landtsharevalue = db.Column(db.Float, nullable=False)
    zeemediasharevalue = db.Column(db.Float, nullable=False)
    techmahindrasharevalue = db.Column(db.Float, nullable=False)
    ashokleylandsharevalue = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Data('{self.timeline}' '{self.tcssharevalue}' '{self.reliancesharevalue}' '{self.infosyssharevalue}' '{self.wiprosharevalue}' '{self.sbisharevalue}' '{self.hdfcsharevalue}' '{self.landtsharevalue}' '{self.zeemediasharevalue}' '{self.techmahindrasharevalue}' '{self.ashokleylandsharevalue}')" 


class Amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Amount('{self.amount}')"
