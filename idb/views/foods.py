from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food
from idb import db

foods = Blueprint('foods', __name__)


@foods.route("/")
def overview():
    # Really just show the first page, but don't use reroute() because
    # we want to keep the pretty URL
    return overview_page(1)


@foods.route("/page/<int:page>")
def overview_page(page):
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
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)

    return render_template('foods/fooddetail.html', food=food)
