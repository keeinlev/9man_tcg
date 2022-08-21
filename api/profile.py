from flask import Blueprint, request, json, url_for, redirect, render_template, flash
from flask_login import login_required, current_user
from app import app, db, BASE_URL as base_url, STATIC_URL as static_url
from models.userModel import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/")
@login_required
def profile():
    if request.method == "GET":
        user = request.args.get("user", None)
        if user is None:
            flash("Error while trying to access user profile.")
            return redirect(url_for('home'))

        got_user = User.query.filter_by(username=user).first()
        if got_user:
            return render_template("profile.html", user=got_user)
        else:
            flash("User not found")
            return redirect(url_for('home'))
    else:
        flash("Invalid method")
        return redirect(url_for('home'))

@profile_bp.route("/trades")
@login_required
def user_trades():
    if request.method == "GET":
        user = request.args.get("user", None)
        if user is None:
            flash("Error while trying to access user trades.")
            return redirect(url_for('home'))
        if user != current_user.username:
            flash("You are not authorized to access this page.")
            return redirect(url_for('home'))
        return render_template("user_trades.html", user=current_user)
    else:
        flash("Invalid method")
        return redirect(url_for('home'))