from flask import current_app as app
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts
from idb import db
from string import capwords
import requests
import json

workouts = Blueprint('workouts', __name__)


@workouts.route("/", defaults={'page': 1, 'sort': 'name'})
@workouts.route("/page/<int:page>")
@workouts.route("/sort/<string:sort>", defaults={'page': 1})
@workouts.route("/sort/<string:sort>/<int:page>")
def overview(page, sort):
    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    get_workouts = db.session.query(Workouts).order_by(getattr(Workouts, sort)).limit(items_per_page).offset((page - 1) * items_per_page).all()
    last_page = db.session.query(Workouts).count() / items_per_page
    for workout in get_workouts:
        if workout.name != "":
            items.append(create_item(workout))

    return render_template('workouts/workouts.html', items=items, sort=sort, current_page=page, last_page=last_page)


@workouts.route("/<int:id>")
def detail(id):
    workout = db.session.query(Workouts).get(id)
    if workout is None:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=workout)


def create_item(raw):
    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = item['img']
    item.pop('_sa_instance_state', None)
    item.pop('img', None)
    item.pop('description', None)
    item.pop('link', None)
    item.pop('equipment', None)
    item.pop('muscles', None)

    return item
