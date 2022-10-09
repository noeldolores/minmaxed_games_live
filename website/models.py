from sqlalchemy.dialects.mysql import DECIMAL
from datetime import datetime
from . import db


class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    server_id = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship('Item', backref=db.backref('market'))
    
    
class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  item_id = db.Column(db.String(150))
  name = db.Column(db.String(150))
  price = db.Column(DECIMAL(38,15))
  availability = db.Column(db.Integer)
  market_id = db.Column(db.Integer, db.ForeignKey(Market.id))