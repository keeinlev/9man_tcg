from flask import Blueprint, request, render_template, redirect, json, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import or_

from app import db
from models.userModel import User

auth = Blueprint('auth', __name__)

def validate_email_pass(email, password):
    """
    Checks if email belongs to existing user and if password is correct for that user
    Return value type -> User <Object>, None, or 0
    Returns User object on success
    Returns None on fail if email does not belong to a user
    Returns 0 on fail if email belongs to user but password is not a match
    """
    if not email:
        return None
    if not password:
        return 0

    got_user = User.query.filter_by(email=email).first()

    if got_user is None:
        return None
    if not check_password_hash(got_user.password, password):
        return 0
    return got_user

def authorized_request(data):
    """
    Given request data return True if valid admin credentials are given or admin is logged in and False otherwise
    """
    got_user = User.query.get(current_user.get_id())
    if (data.get("email", None) is not None and data.get("password", None) is not None):
        got_user = validate_email_pass(data.get("email", None), data.get("password", None))
    if ((not got_user and not current_user.is_authenticated) or not got_user.is_admin):
        return False
    return True

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

    got_user = validate_email_pass(email, password)

    # wrong email
    if got_user is None:
        flash("Email not found")
        return redirect(url_for("auth.login"))
    
    # wrong password
    if got_user == 0:
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

        new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"), timezone=local_tz, date_created=datetime.utcnow(), is_active=True, is_admin=False)
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