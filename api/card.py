from flask import request, json
from app import app, db, BASE_STATIC_URL as base_url
from models.cardModel import Card

@app.route("/card", methods=['GET', 'POST'])
def card_get_post():
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
        params = (
            data.get("name", None),
            data.get("team", None),
            data.get("year", 2022),
            data.get("collection", "2022 Season"),
            data.get("image_url", base_url + "/static/images/null.png"),
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
        INSERT INTO cards 
            (name, team, year, collection, image_url, rarity) 
        VALUES 
            (?, ?, ?, ?, ?, ?) 
        RETURNING id;
        """
        result = cursor.execute(query, params).fetchall()[0]
        #result = db.engine.execute("INSERT INTO cards (name, team, year, collection, image_url) VALUES (\"Kevin Lee\", \"TUV\", 2022, \"TUV Mini\", \"none\");")
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "status": "success",
            "message": "New player card created", 
            "id": result[0]
        }
    elif request.method == "GET":
        card_id = request.args.get('id', None)
        if card_id is None:
            return {"status": "failed", "message": "Card with specified ID could not be found"}
        got_card = Card.query.get(card_id)
        if got_card:
            return {"status": "success", "name": Card.query.get(card_id).name}
        else:
            return {"status": "failed", "message": "Card with specified ID could not be found"}
    else:
        return {"status": "failed", "message": "Request method not supported"}