from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food
from idb import db

foods = Blueprint('foods', __name__)

first = 0
last = 99999999999


@foods.route("/")
def foods_overview():
    # Really just show the first page, but don't use reroute() because
    # we want to keep the pretty URL
    return foods_overview_page(1)


@foods.route("/page/<int:page>")
def foods_overview_page(page):
    items_per_page = 20
    items = []
    get_foods = db.session.query(Food).limit(items_per_page).offset((page - 1) * items_per_page).all()
    last_page = db.session.query(Food).count() / items_per_page
    for val in get_foods:
        image = 'https://spoonacular.com/cdn/ingredients_500x500/' + val.img
        items.append([val.name.title(), image, val.calorie, val.fat, val.id])

    return render_template('foods/food.html', items=items, current_page=page, last_page=last_page)


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
