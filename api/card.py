from flask import Blueprint, request, json
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime
from app import db, BASE_URL as base_url, STATIC_URL as static_url
from auth import authorized_request
from models.cardModel import Card

card_bp = Blueprint('card', __name__)

@card_bp.route("/create", methods=['POST'])
def create_card():
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
        
        now = datetime.utcnow()
        params = {
            "template_id": data.get("template_id", None),
            "owner": data.get("owner", None),
            "date_created": now,
            "date_received": now,
        }
        if params["template_id"] is None:
            return {"status": "failed", "message": "Missing required fields 'template_id'"}
        elif params["owner"] is None:
            return {"status": "failed", "message": "Missing required fields 'owner'"}
        
        try:
            new_card = Card(**params)
            db.session.add(new_card)
            db.session.commit()
        except IntegrityError:
            return {"status": "failed", "message": "Database IntegrityError"}
        except OperationalError:
            return {"status": "failed", "message": "Database OperationalError"}
        
        return {
            "status": "success",
            "message": "New card created", 
            "id": new_card.id,
            "owner": new_card.owner,
            "template_id": new_card.template_id,
        }
