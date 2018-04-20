from flask import current_app as app
from flask import Blueprint, render_template, abort, jsonify, request
from sqlalchemy import or_, func
from idb.models import Food, Workouts, Stores, Images
from idb import db
from string import capwords
from math import ceil

from .db_functions import gen_query
from backend.tools import unbinary
import base64

foods = Blueprint('foods', __name__)


@foods.route("/")
def overview():
    """
    The overview page for foods that shows all of the foods in the
    database.
    """
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    filters = request.args.get('filters', default="", type=str)

    attributes = [Food.aisle, Food.aisle2, Food.aisle3]
    cat = db.session.query(Food).distinct(attributes[0])
    f_crit = {c.aisle for c in cat}

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)

    query = gen_query(Food, items_per_page, page, sort, order, attributes, filters)
    total_count = gen_query(Food, 10000000, 1, sort, order, attributes, filters).count()

    get_foods = query.all()
    items = [create_item(food) for food in get_foods]
    last_page = ceil(total_count / items_per_page)

    return render_template('foods/food.html', items=items, sort=sort, order=order, filters=filters, current_page=page, last_page=last_page, f_crit=f_crit)


@foods.route("/<int:id>")
def detail(id):
    """
    The individual detail page for foods that show all of the information
    we have about a food item.
    """
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)
    food.name = capwords(food.name)

    query = db.session.query(Food).filter(Food.aisle == food.aisle, Food.name != food.name).order_by(func.random()).limit(4)
    get_foods = query.all()
    similar_foods = [create_item(s) for s in get_foods]

    workout = db.session.query(Workouts).filter(or_(Workouts.category == "conditioning exercise", Workouts.category == "sports", Workouts.category == "bicycling")).order_by(func.random()).limit(4)
    workouts = [item for item in workout]

    stores = []
    images = []
    store_query = db.session.query(Stores).order_by(func.random()).limit(4)
    for store in store_query:
        stores.append(store)
        image = db.session.query(Images).get(store.pic_id).pic
        img = unbinary(str(base64.b64encode(image)))
        images.append(img)

    return render_template('foods/fooddetail.html', food=food, similar_foods=similar_foods, workouts=workouts, stores=stores, images=images)


def create_item(raw):
    """
    Create a dictionary item that represents the database item with
    some of the spurious things like internal ids and such for 
    presentation and organization on the actual site.  Also do any
    preprocessing like determing the URL for the detail page or processing
    images before being displayed.
    """

    image = 'https://spoonacular.com/cdn/ingredients_500x500/' + raw.img

    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw).copy()  # and don't alter the real thing
    item['name'] = capwords(item['name'])
    item['image'] = image
    item['detail_url'] = "foods/" + str(item['id'])

    item['aisle'] = item['aisle']
    if item['aisle2'] is not None:
        item['aisle'] += "; " + item['aisle2']
    if item['aisle3'] is not None:
        item['aisle'] += "; " + item['aisle3']
    item.pop('aisle2')
    item.pop('aisle3')
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('servings', None)

    return item
