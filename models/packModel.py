from app import db

class Pack(db.Model):
    __tablename__ = "packs"
    id = db.Column(db.Integer, primary_key=True)
    num_cards = db.Column(db.Integer, nullable=False)
    collection = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    __table_args__ = (
        db.CheckConstraint(num_cards > 0, name='check_num_cards_positive'),)