from app import db
from models.cardModel import Card
from sqlalchemy import and_

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False) # either "pack", "trade" or "friend"
    seen = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    event_id = db.Column(db.Integer, nullable=False) # pack, trade, friendship id
