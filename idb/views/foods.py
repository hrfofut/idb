from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food
from idb import db

foods = Blueprint('foods', __name__)

first = 0
last = 99999999999


@foods.route("/", subdomain='api')
def food_api():
    foods = db.session.query(Food).all()

    food_json = list()

    for food in foods:
        food_dict = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein}
        food_json.append(food_dict)

    return jsonify(food_json)


@foods.route("/")
def foods_overview():
    # TODO: I need to remember to describe whats going on later.
    items = []
    get_foods = db.session.query(Food).all()
    for val in get_foods:
        image = 'https://spoonacular.com/cdn/ingredients_500x500/' + val.img
        items.append([val.name.title(), image, val.calorie, val.fat, val.id])

    return render_template('foods/food.html', items=items)


@foods.route("/<int:id>")
def food_detail(id):
    global last
    """TODO: Have the template be filled from a database in the future"""
    # However the backend will work, use id to find all the info.

    if last == -1:
        last = db.session.query(Food).count()

    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return abort(404)

    return render_template('foods/fooddetail.html', food=db.session.query(Food).get(id))
