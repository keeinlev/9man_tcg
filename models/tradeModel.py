from app import db

cardsInTrades = db.Table('cards_to_trade',
    db.Column('trade_id', db.ForeignKey('trades.id'), primary_key=True),
    db.Column('card_id', db.ForeignKey('cards.id'), primary_key=True),
    db.Column('is_sender', db.Boolean, nullable=False)
)

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', secondary=cardsInTrades, lazy='subquery')
    date_created = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)
    accepted = db.Column(db.Boolean, nullable=False)