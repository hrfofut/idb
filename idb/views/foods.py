from flask import current_app as app
from flask import Blueprint, render_template, abort, jsonify, request, url_for
from idb.models import Food
from idb import db
from string import capwords
from math import ceil
from .db_functions import gen_query

foods = Blueprint('foods', __name__)


@foods.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []

    query = gen_query(Food, items_per_page, page, sort, order)
    get_foods = query.all()

    last_page = ceil(db.session.query(Food).count() / items_per_page)
    for food in get_foods:
        items.append(create_item(food))

    return render_template('foods/food.html', items=items, sort=sort, current_page=page, last_page=last_page)


@foods.route("/<int:id>")
def detail(id):
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)
    food.name = capwords(food.name)
    return render_template('foods/fooddetail.html', food=food)


def create_item(raw):
    image = 'https://spoonacular.com/cdn/ingredients_500x500/' + raw.img

    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = image
    item['detail_url'] = url_for('foods.detail', id=item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('servings', None)

    return item
