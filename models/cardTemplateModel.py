from app import db
from datetime import datetime

class CardTemplate(db.Model):
    __tablename__ = "card_templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    collection = db.Column(db.String(50), nullable=False, default=str(datetime.now().year) + " Season")
    rarity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
