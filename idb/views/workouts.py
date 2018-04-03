from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts
from idb import db
import requests
import json

workouts = Blueprint('workouts', __name__)

first = 0
last = 100000000  # This is bad design.


@workouts.route("/")
def overview():
    # Really just show the first page, but don't use reroute() because
    # we want to keep the pretty URL
    return overview_page(1)


@workouts.route("/page/<int:page>")
def overview_page(page):
    items_per_page = 20
    items = []
    get_workouts = db.session.query(Workouts).limit(items_per_page).offset((page - 1) * items_per_page).all()
    last_page = db.session.query(Workouts).count() / items_per_page
    print(last_page)
    for val in get_workouts:
        if val.name != "":
            items.append([val.name, val.img, val.category, val.muscle, val.id])

    return render_template('workouts/workouts.html', items=items, current_page=page, last_page=last_page)


@workouts.route("/<int:id>")
def workouts_detail(id):
    global last
    # Somehow we should find a better way to tell if the page doesn't exist, probably check if the get worked.
    if id < first or id > last:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=db.session.query(Workouts).get(id))
