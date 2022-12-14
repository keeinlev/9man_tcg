from app import db
from models.cardTemplateModel import CardTemplate

class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.ForeignKey('card_templates.id', ondelete="CASCADE"), nullable=False)
    owner = db.Column(db.String(100), nullable=False) # username
    date_created = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)

    @property
    def name(self):
        return CardTemplate.query.get(self.template_id).name