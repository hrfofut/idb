from flask import Blueprint, render_template, abort, g
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts
from idb import db
import requests
import json

workouts = Blueprint('workouts', __name__)

first = 0
last = 100000000


@workouts.route("/")
def workouts_overview():

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
    # TODO: Have the template be filled from a database in the future
    # ID 0-2 returns certain food page, else return error

    if id < first or id > last:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=db.session.query(Workouts).get(id))
