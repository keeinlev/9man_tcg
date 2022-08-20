from flask import Blueprint, request, render_template, redirect, json, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import or_

from app import db
from models.userModel import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html", signup=(True if request.args.get("signup", None) else False))

    # POST
    email = request.form.get("email", None)
    password = request.form.get("password", None)
    remember = True if request.form.get('remember') else False
    if not email or not password:
        flash("Please fill in all fields")
        return redirect(url_for("auth.login"))

    got_user = User.query.filter_by(email=email).first()

    # wrong email
    if got_user is None:
        flash("Email not found")
        return redirect(url_for("auth.login"))
    
    # wrong password
    if not check_password_hash(got_user.password, password):
        flash("Password incorrect")
        return redirect(url_for("auth.login"))

    login_user(got_user, remember=remember)
    return redirect("/")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        data = None
        if not request.form:
            flash("No arguments given.")
            return redirect(url_for("auth.signup"))
        data = request.form

        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        local_tz = data.get("timezone", None)

        if not email or not username or not password:
            flash("Please fill out all fields.")
            return redirect(url_for("auth.signup"))

        if User.query.filter(or_(User.email == email, User.username == username)).first() is not None:
            flash("User with that email or username already exists.")
            return redirect(url_for("auth.signup"))

        new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"), timezone=local_tz, date_created=datetime.utcnow(), is_active=True)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login", signup=True))

    # GET
    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("login")