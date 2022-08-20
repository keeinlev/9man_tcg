from flask import request, json
from flask_login import current_user
from app import app, db, BASE_URL as base_url, STATIC_URL as static_url
from auth import validate_email_pass
from models.cardTemplateModel import CardTemplate

@app.route("/card", methods=['GET', 'POST'])
def card_template_get_post():
    if request.method == "POST":
        data = None
        if request.data:
            print("using data")
            data = json.loads(request.data) # maybe use request.form if this is going to be on an interface
        elif request.form:
            print("using form")
            data = request.form
        else:
            return {"status": "failed", "message": "No arguments given"}

        if (data.get("email", None) is not None and data.get("password", None) is not None):
            got_user = validate_email_pass(data.get("email", None), data.get("password", None))
        if not ((current_user.is_authenticated and current_user.is_admin) or (got_user and got_user.is_admin)):
            return {"status": "failed", "message": "User is not authorized to perform this action."}
        params = (
            data.get("name", None),
            data.get("team", None),
            data.get("year", 2022),
            data.get("collection", "2022 Season"),
            data.get("image_url", static_url + "/images/null.png"),
            data.get("rarity", None),
        )
        if params[0] is None:
            return {"status": "failed", "message": "Missing required fields 'name'"}
        elif params[1] is None:
            return {"status": "failed", "message": "Missing required fields 'team'"}
        elif params[5] is None:
            return {"status": "failed", "message": "Missing required fields 'rarity'"}

        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO card_templates 
            (name, team, year, collection, image_url, rarity) 
        VALUES 
            (?, ?, ?, ?, ?, ?) 
        RETURNING id;
        """
        result = cursor.execute(query, params).fetchall()[0]
        #result = db.engine.execute("INSERT INTO card_templates (name, team, year, collection, image_url) VALUES (\"Kevin Lee\", \"TUV\", 2022, \"TUV Mini\", \"none\");")
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "status": "success",
            "message": "New player card created", 
            "id": result[0]
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

# @app.route("")
# def create_card()