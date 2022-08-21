from flask import render_template
from datetime import datetime
from models.cardTemplateModel import CardTemplate
from models.cardModel import Card
from models.packModel import Pack
from models.tradeModel import Trade
from models.userModel import User, FriendshipAssoc
from app import app, db
from api.card import *
from api.profile import *
from api.search import *
from tests import *
from auth import *

db.create_all()
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/auth")
from api.card import card_bp as card_blueprint
app.register_blueprint(card_blueprint, url_prefix="/card")

@app.route("/")
def home():
    return render_template("index.html")

def start_flask():
    app.run(host="127.0.0.1", port="5000", debug=True)

if __name__=="__main__":
    if app.config['TESTING']:
        clear_db()
        friendshipRelationshipTest()
        tradeRelationshipTest()
    start_flask()