from flask import request, json
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime
from app import db, BASE_URL as base_url, STATIC_URL as static_url
from auth import authorized_request
from models.cardTemplateModel import CardTemplate
from api.card import card_bp

@card_bp.route("/template", methods=['GET', 'POST'])
def card_template_get_post():
    if request.method == "POST":
        data = None
        if request.data:
            data = json.loads(request.data)
        elif request.form:
            data = request.form
        else:
            return {"status": "failed", "message": "No arguments given"}

        if not authorized_request(data):
            return {"status": "failed", "message": "User is not authorized to perform this action."}

        params = {
            "name": data.get("name", None),
            "team": data.get("team", None),
            "year": data.get("year", 2022),
            "collection": data.get("collection", "2022 Season"),
            "image_url": data.get("image_url", static_url + "/images/null.png"),
            "rarity": data.get("rarity", None),
        }
        if params["name"] is None:
            return {"status": "failed", "message": "Missing required fields 'name'"}
        elif params["team"] is None:
            return {"status": "failed", "message": "Missing required fields 'team'"}
        elif params["image_url"] is None:
            return {"status": "failed", "message": "Missing required fields 'rarity'"}

        try:
            new_template = CardTemplate(**params)
            db.session.add(new_template)
            db.session.commit()
        except IntegrityError:
            return {"status": "failed", "message": "Card with that name, team, year, collection combination already exists"}
        except OperationalError:
            return {"status": "failed", "message": "Database OperationalError"}

        return {
            "status": "success",
            "message": "New player card created", 
            "id": new_template.id
        }
    elif request.method == "GET":
        template_id = request.args.get('id', None)
        if template_id is None:
            return {"status": "failed", "message": "Card with specified ID could not be found"}
        got_card = CardTemplate.query.get(template_id)
        if got_card:
            return {"status": "success", "name": CardTemplate.query.get(template_id).name}
        else:
            return {"status": "failed", "message": "Card with specified ID could not be found"}
    else:
        return {"status": "failed", "message": "Request method not supported"}
