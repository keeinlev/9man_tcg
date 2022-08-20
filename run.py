from flask import render_template
from models.cardTemplateModel import CardTemplate
from models.cardModel import Card
from models.packModel import Pack
from models.tradeModel import Trade
from app import app, db
from api.card import *
from api.profile import *
from auth import *

db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

def start_flask():
    app.run(host="127.0.0.1", port="5000", debug=True)

if __name__=="__main__":
    start_flask()