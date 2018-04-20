from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from idb.models import Workouts, Food, Gyms, Images
from idb import db
from string import capwords
import requests
import json
from math import ceil

from .db_functions import gen_query
from .foods import create_item as food_create_item
from backend.tools import unbinary
import base64

workouts = Blueprint('workouts', __name__)


@workouts.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    filters = request.args.get('filters', default='', type=str)

    attributes = [Workouts.category]

    cat = db.session.query(Workouts).distinct(attributes[0])
    f_crit = set()  # filter criteria
    f_crit = {c.category for c in cat}

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)

    query = gen_query(Workouts, items_per_page, page, sort, order, attributes, filters)
    total_count = gen_query(Workouts, 10000000, 1, sort, order, attributes, filters).count()

    get_workouts = query.all()
    items = [create_item(workout) for workout in get_workouts]
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
    query = db.session.query(Food).filter(Food.calorie.between(calorie - 50, calorie + 50)).order_by(func.random()).limit(4)
    get_foods = query.all()
    for food in get_foods:
        foods.append(food_create_item(food))

    similar_workouts = []
    workout_query = db.session.query(Workouts).filter(Workouts.category == workout.category, Workouts.name != workout.name).order_by(func.random()).limit(4)
    for sim_workout in workout_query:
        similar_workouts.append(sim_workout)

    gyms = []
    images = []
    # TODO: Add gyms that have this workouts
    if workout.category == "conditioning exercise":
        gym_query = db.session.query(Gyms).order_by(func.random()).limit(4)
        for gym in gym_query:
            gyms.append(gym)
            image = db.session.query(Images).get(gym.pic_id).pic
            img = unbinary(str(base64.b64encode(image)))
            images.append(img)

    return render_template('workouts/workoutsdetail.html', workout=workout, foods=foods, similar_workouts=similar_workouts, gyms=gyms, images=images)


def create_item(raw):
    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw).copy()  # and don't alter the real thing
    item['name'] = capwords(item['name'])
    item['image'] = item['img']
    item['detail_url'] = "workouts/" + str(item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('description', None)
    item.pop('cid', None)
    item.pop('parent', None)

    return item
