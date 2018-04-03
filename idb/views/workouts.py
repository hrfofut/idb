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
    items = []
    get_workouts = db.session.query(Workouts).all()
    for val in get_workouts:
        if val.name != "":
            items.append([val.name, val.img, val.category, val.muscle, val.id])
    # grab data from api
    # exercises = get_exercises(items)
    return render_template('workouts/workouts.html', items=items)


@workouts.route("/<int:id>")
def workouts_detail(id):
    global last
    # Somehow we should find a better way to tell if the page doesn't exist, probably check if the get worked.
    if id < first or id > last:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=db.session.query(Workouts).get(id))
