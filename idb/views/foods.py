from flask import current_app as app
from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food
from idb import db
from string import capwords

foods = Blueprint('foods', __name__)
asc = True


@foods.route("/", defaults={'page': 1, 'sort': 'name'})
@foods.route("/page/<int:page>")
@foods.route("/sort/<string:sort>", defaults={'page': 1})
@foods.route("/sort/<string:sort>/<int:page>")
def overview(page, sort):
    global asc
    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    if(asc):
        get_foods = db.session.query(Food).order_by(getattr(Food, sort)).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = False
    else:
        get_foods = db.session.query(Food).order_by(getattr(Food, sort).desc()).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = True

    last_page = db.session.query(Food).count() / items_per_page
    for food in get_foods:
        items.append(create_item(food))

    return render_template('foods/food.html', items=items, sort=sort, current_page=page, last_page=last_page)


@foods.route("/<int:id>")
def detail(id):
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)

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
