from app import db
from models.cardModel import Card
from models.packModel import Pack
from sqlalchemy import and_

cardsInTradesAssoc = db.Table(
    'cards_to_trade',
    db.Column('trade_id', db.ForeignKey('trades.id'), primary_key=True),
    db.Column('card_id', db.ForeignKey('cards.id'), primary_key=True)
)

packsInTradesAssoc = db.Table(
    'packs_to_trade',
    db.Column('trade_id', db.ForeignKey('trades.id'), primary_key=True),
    db.Column('pack_id', db.ForeignKey('packs.id'), primary_key=True)
)

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', secondary=cardsInTradesAssoc)
    packs = db.relationship('Pack', secondary=packsInTradesAssoc)
    date_created = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)
    accepted = db.Column(db.Boolean, nullable=False)

    def other_user(self, known_user):
        if known_user != self.sender and known_user != self.receiver:
            return None
        return (self.sender if known_user == self.receiver else self.receiver)

    @property
    def card_ids(self):
        return [ c.id for c in self.cards ]
    
    @property
    def pack_ids(self):
        return [ p.id for p in self.packs ]

    @property
    def sender_cards(self):
        return Card.query.filter(and_(Card.id.in_(self.card_ids), Card.owner == self.sender)).all()

    @property
    def receiver_cards(self):
        return Card.query.filter(and_(Card.id.in_(self.card_ids), Card.owner == self.receiver)).all()

    @property
    def grouped_cards(self):
        return (self.sender_cards, self.receiver_cards)
        
    @property
    def sender_packs(self):
        return Pack.query.filter(and_(Pack.id.in_(self.pack_ids), Pack.owner == self.sender)).all()

    @property
    def receiver_packs(self):
        return Pack.query.filter(and_(Pack.id.in_(self.pack_ids), Pack.owner == self.receiver)).all()

    @property
    def grouped_packs(self):
        return (self.sender_packs, self.receiver_packs)
    
    @property
    def grouped_items(self):
        return (self.grouped_cards, self.grouped_packs)