from app import db

class CollectibleCard(db.Model):
    __tablename__ = "collectible_cards"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.ForeignKey('cards.id', ondelete="CASCADE"), nullable=False)
    owner_user = db.Column(db.String(100), nullable=False) # username
    date_created = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)