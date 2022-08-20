from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_URL = "http://127.0.0.1:5000"
STATIC_URL = "/static"


db = SQLAlchemy(app)

db.init_app(app)
