from app import db
from models.cardModel import Card
from sqlalchemy import and_

cardsInTradesAssoc = db.Table(
    'cards_to_trade',
    db.Column('trade_id', db.ForeignKey('trades.id'), primary_key=True),
    db.Column('card_id', db.ForeignKey('cards.id'), primary_key=True)
)

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', secondary=cardsInTradesAssoc)
    date_created = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)
    accepted = db.Column(db.Boolean, nullable=False)

    @property
    def card_ids(self):
        return [ c.id for c in self.cards ]

    @property
    def sender_cards(self):
        return Card.query.filter(and_(Card.id.in_(self.card_ids), Card.owner == self.sender)).all()

    @property
    def receiver_cards(self):
        return Card.query.filter(and_(Card.id.in_(self.card_ids), Card.owner == self.receiver)).all()

    @property
    def grouped_cards(self):
        return (self.sender_cards, self.receiver_cards)