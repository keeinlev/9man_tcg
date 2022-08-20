from flask import request, json, url_for, redirect, render_template
from flask_login import login_required
from app import app, db, BASE_URL as base_url, STATIC_URL as static_url
from models.userModel import User

@app.route("/profile")
@login_required
def profile():
    if request.method == "GET":
        user_id = request.args.get("user", None)
        if user_id is None:
            flash("Error while trying to access user profile.")
            return redirect("/")

        got_user = User.query.get(user_id)
        if got_user:
            return render_template("profile.html", user=got_user)
        else:
            flash("User not found")
            return redirect("/")
    else:
        flash("Invalid method")
        return redirect("/")