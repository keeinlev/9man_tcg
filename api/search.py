from flask import request, json, url_for, redirect, render_template, flash
from flask_login import login_required
from app import app, db, BASE_URL as base_url, STATIC_URL as static_url
from models.userModel import User

@app.route("/search")
@login_required
def search():
    if request.method == "GET":
        query_string = request.args.get("query_string", None)
        if query_string is None:
            return render_template("search.html")
        if query_string == "":
            return {"status": "success", "users": []}
        queried_users = User.query.filter(User.username.ilike(f'%{query_string}%'))
        # don't want to go thru trouble of creating a SQLAlchemy Row -> json encoding, also querying specific columns doesn't give __dict__ property
        desired_fields = ["id", "username", "date_created"]
        return {
            "status": "success",
            "users": [ dict(filter(lambda pair: pair[0] in desired_fields, u.__dict__.items())) for u in queried_users ]
        }
    else:
        flash("Request method not supported")
        return redirect(url_for("search"), status="failed")
