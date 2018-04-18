from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts, Food
from idb import db
from string import capwords
import requests
import json
from math import ceil

from .db_functions import gen_query
from .foods import create_item as food_create_item

workouts = Blueprint('workouts', __name__)


@workouts.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    filters = request.args.get('filters', default='', type=str)

    attribute = Workouts.category

    cat = db.session.query(Workouts).distinct(attribute)
    f_crit = set()  # filter criteria
    for c in cat:
        f_crit.add(c.category)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []

    query = gen_query(Workouts, items_per_page, page, sort, order, attribute, filters)
    total_count = gen_query(Workouts, 10000000, 1, sort, order, attribute, filters).count()

    get_workouts = query.all()
    for workout in get_workouts:
        # if workout.parent is None: #Only include excercises that are the original. This doesn't actually work because gen_query only every returns 20 objects.
        item = create_item(workout)
        items.append(item)
    last_page = ceil(total_count / items_per_page)

    return render_template('workouts/workouts.html', items=items, sort=sort, order=order, filters=filters, current_page=page, last_page=last_page, f_crit=f_crit)


@workouts.route("/<int:id>")
def detail(id):
    workout = db.session.query(Workouts).get(id)
    if workout is None:
        abort(404)
    workout.name = capwords(workout.name)

    # calculate number of calories that would be burned off for an average person in an hour
    calorie = workout.met * 62

    foods = []
    query = db.session.query(Food).filter(Food.calorie.between(calorie - 50, calorie + 50)).limit(4)
    get_foods = query.all()
    for food in get_foods:
        foods.append(food_create_item(food))

    return render_template('workouts/workoutsdetail.html', workout=workout, foods=foods)


def create_item(raw):
    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = item['img']
    item['detail_url'] = "workouts/" + str(item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('description', None)
    item.pop('cid', None)
    item.pop('parent', None)

    return item
