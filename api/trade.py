from flask import request, json, url_for, redirect, render_template, flash
from flask_login import login_required, current_user
from app import app, db, BASE_URL as base_url, STATIC_URL as static_url
from models.userModel import User
from models.cardModel import Card
from models.packModel import Pack
from models.tradeModel import Trade
from models.notificationModel import Notification

@app.route("/trade", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def trade():
    trade_id = request.args.get("trade_id", None)
    other_user = request.args.get("other_user", None)
    if request.method == "GET":
        # steps:
        #   - see if trade_id or other_user is set
        #       - trade_id -> trade exists, preload trade page with trade config
        #       - other_user -> creating new trade with this user, load empty trade page, create Trade object upon submission
        #       - these two must be exclusive or
        #   - check that trade/user exists in db
        #   - if editing trade, check that current user is either the sender or receiver of the trade
        #   - if creating new trade, check that receiver user is friend of current user
        if trade_id is not None and other_user is None:
            t = Trade.query.get(trade_id)
            if not t:
                flash("Trade not found.")
                return redirect(url_for("profile", user=current_user.username))
            if t.sender != current_user.username and t.receiver != current_user.username:
                flash("You are not authorized to access this page.")
                return redirect(url_for("profile.profile", user=current_user.username))
            return render_template("trade.html", trade=t, edit=True)
        elif other_user is not None and trade_id is None:
            got_user = User.query.filter_by(username=other_user).first()
            if not got_user:
                flash("User not found")
                return redirect(url_for("profile.profile", user=current_user.username))
            if not current_user.is_friends_with(other_user):
                flash("You cannot send trades to users that are not your friend.")
                return redirect(url_for("profile.profile", user=current_user.username))
            return render_template("trade.html", other_user=got_user, edit=False)
        else:
            flash("Invalid argument configuration.")
            return redirect(url_for("profile.profile", user=current_user.username))

    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        return {"status": "failed", "message": "Request method not supported."}

