from models.cardModel import Card
from models.cardTemplateModel import CardTemplate
from models.tradeModel import Trade
from models.userModel import User, FriendshipAssoc
from app import app, db
from datetime import datetime

now = datetime.utcnow()

def clear_db():
    db.session.commit()
    db.drop_all()
    db.create_all()

def friendshipRelationshipTest():
    u1 = User(email="kvld@live.ca", username="kevinlee", password="", is_active=True, is_admin=True, date_created=now, timezone_std=-5, timezone_dst=-4)
    u2 = User(email="kevin348960@gmail.com", username="kevinlee2", password="", is_active=True, is_admin=False, date_created=now, timezone_std=-5, timezone_dst=-4)
    u3 = User(email="kevin.l@scentroid.com", username="kevinlee3", password="", is_active=True, is_admin=False, date_created=now, timezone_std=-5, timezone_dst=-4)
    u1.set_password("asdf")
    u2.set_password("asdf")
    u3.set_password("asdf")
    db.session.add_all([u1, u2, u3])
    f1 = FriendshipAssoc(friend_a="kevinlee", friend_b="kevinlee2", date_created=now, date_accepted=now)
    f2 = FriendshipAssoc(friend_a="kevinlee", friend_b="kevinlee3", date_created=now)
    db.session.add_all([f1, f2])
    db.session.commit()
    print(u1.friends, u2.friends)

def tradeRelationshipTest():
    template = CardTemplate(name="test1", year=2022, team="TUV", collection="test1", rarity=1, image_url="")
    db.session.add(template)
    card1 = Card(owner="kevinlee", template_id=1, date_created=now, date_received=now)
    card2 = Card(owner="kevinlee2", template_id=1, date_created=now, date_received=now)
    card3 = Card(owner="kevinlee2", template_id=1, date_created=now, date_received=now)
    t1 = Trade(sender="kevinlee", receiver="kevinlee2", date_created=now, accepted=False)
    t1.cards.append(card1)
    t1.cards.append(card2)
    t1.cards.append(card3)
    db.session.add_all([card1, card2, card3])
    db.session.add(t1)
    db.session.commit()
    print(t1.grouped_cards)