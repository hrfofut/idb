from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food
from idb import db

api = Blueprint('api', __name__)


@api.route("/", subdomain="<api>")
def food_api(api):
    foods = db.session.query(Food).all()

    food_json = list()

    for food in foods:
        food_dict = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein}
        food_json.append(food_dict)

    return jsonify(food_json)
