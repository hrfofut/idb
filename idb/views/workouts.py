from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts
from idb import db
from string import capwords
import requests
import json
from math import ceil

workouts = Blueprint('workouts', __name__)


@workouts.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    query = db.session.query(Workouts)
    if order == 'desc':
        query = query.order_by(getattr(Workouts, sort).desc())
    else:
        query = query.order_by(getattr(Workouts, sort))
    query = (query
             .limit(items_per_page)
             .offset((page - 1) * items_per_page))

    get_workouts = query.all()
    last_page = ceil(db.session.query(Workouts).count() / items_per_page)
    for workout in get_workouts:
        if workout.name != "":
            items.append(create_item(workout))

    return render_template('workouts/workouts.html', items=items, sort=sort, current_page=page, last_page=last_page)


@workouts.route("/<int:id>")
def detail(id):
    workout = db.session.query(Workouts).get(id)
    if workout is None:
        abort(404)
    workout.name = capwords(workout.name)
    return render_template('workouts/workoutsdetail.html', workout=workout)


def create_item(raw):
    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = item['img']
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('description', None)

    return item
