from flask import current_app as app
from flask import Blueprint, render_template, abort, jsonify, request
from idb.models import Food
from idb import db
from string import capwords
from math import ceil

foods = Blueprint('foods', __name__)


@foods.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    query = db.session.query(Food)
    if order == 'desc':
        query = query.order_by(getattr(Food, sort).desc())
    else:
        query = query.order_by(getattr(Food, sort))
    query = (query
             .limit(items_per_page)
             .offset((page - 1) * items_per_page))

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
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('servings', None)

    return item
