from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import and_, or_
from app import db
from models.cardModel import Card
from models.packModel import Pack
from models.tradeModel import Trade
from datetime import timedelta, datetime
from util import nth_weekday_of_month

# before send request from a to b, check:
#   - if non-pending (accepted) entry between a and b exists -> already friends, don't give option to send
#   - if pending entry between a and b exists -> already sent, disable until further action
# on send request from a to b, check:
#   - if pending request exists from b to a: yes -> accept that one, no -> create new object w/ pending=True
# other user accepts -> change pending to False
# other user declines -> delete table entry
# ONLY ONE ROW PER FRIENDSHIP, CAN BE EITHER DIRECTION, SO CHECK BOTH WAYS WHEN GETTING FRIENDS
class FriendshipAssoc(db.Model):
    __tablename__ = 'friendships'
    friend_a = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)
    friend_b = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False)
    date_accepted = db.Column(db.DateTime)

class User(UserMixin, db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    timezone_std = db.Column(db.Integer, nullable=False, default=0)
    timezone_dst = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")
        db.session.commit()
    
    @property
    def timezone(self):
        now = datetime.now() # use now() b/c dst starts 2am local time for any tz
        dst_start = nth_weekday_of_month(1, 0, 3, now.year) + timedelta(hours=2)
        dst_end = nth_weekday_of_month(1, 0, 11, now.year) + timedelta(hours=2)

        if now >= dst_start and now <= dst_end:
            return self.timezone_dst
        else:
            return self.timezone_std

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def cards(self):
        return Card.query.filter_by(owner=self.username)
    
    @property
    def packs(self):
        return Pack.query.filter_by(owner=self.username)
    
    @property
    def friends(self):
        a_friendships = FriendshipAssoc.query.filter(and_(FriendshipAssoc.friend_a == self.username, FriendshipAssoc.date_accepted != None)).all()
        b_friendships = FriendshipAssoc.query.filter(and_(FriendshipAssoc.friend_b == self.username, FriendshipAssoc.date_accepted != None)).all()
        a_friends = [ f.friend_b for f in a_friendships ]
        b_friends = [ f.friend_a for f in b_friendships ]
        return tuple(a_friends + b_friends) # can do this b/c only have 1 row/friendship, disjoint union
    
    def is_friends_with(self, other):
        return other in self.friends

    def get_friendship(self, other):
        return FriendshipAssoc.query.filter(
            or_(
                and_(FriendshipAssoc.friend_a == self.username, FriendshipAssoc.friend_b == other),
                and_(FriendshipAssoc.friend_b == self.username, FriendshipAssoc.friend_a == other)
            )
        ).first()
    
    def friends_since(self, other):
        if self.is_friends_with(other):
            return (self.get_friendship(other).date_accepted + timedelta(hours=self.timezone)).strftime("%B %d %Y %I:%m %p")
        else:
            return "N/A"
    
    @property
    def sent_trades():
        return Trade.query.filter(Trade.sender == self.username).order_by(Trade.accepted.asc(), Trade.date_created.desc()).all()

    @property
    def received_trades():
        return Trade.query.filter(Trade.sender == self.username).order_by(Trade.accepted.asc(), Trade.date_created.desc()).all()

    @property
    def all_trades():
        return Trade.query.filter(or_(Trade.sender == self.username, Trade.receiver == self.username)).order_by(Trade.accepted.asc(), Trade.date_created.desc()).all()