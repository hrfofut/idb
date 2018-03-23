from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food, Workouts, Stores, Gyms
from idb import db

api = Blueprint('api', __name__)


@api.route("/foods", subdomain="<api>")
def food_api(api):
    foods = db.session.query(Food).all()

    food_json = list()

    for food in foods:
        food_dict = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein}
        food_json.append(food_dict)

    return jsonify(food_json)


@api.route("/workouts", subdomain="<api>")
def workouts_api(api):
    workouts = db.session.query(Workouts).all()

    workout_json = list()

    for workout in workouts:
        workout_dict = {'id': workout.id, 'name': workout.name, 'category': workout.category, 'equipment': workout.equipment, 'description': workout.description, 'muscle': workout.muscle}
        workout_json.append(workout_dict)

    return jsonify(workout_json)


@api.route("/stores", subdomain="<api>")
def stores_api(api):
    stores = db.session.query(Stores).all()

    stores_json = list()

    for store in stores:
        store_dict = {'id': store.id, 'gid': store.gid, 'name': store.name, 'location': store.location, 'price_level': store.price_level, 'ratings': store.ratings}
        store_json.append(store_dict)

    return jsonify(store_json)
