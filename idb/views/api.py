from flask import Blueprint, render_template, abort, jsonify
from idb.models import Food, Workouts, Stores, Gyms
from idb import db

api = Blueprint('api', __name__)


@api.route("/")
def api_splash():
    return "API PAGE"


@api.route("/foods/")
def food_api():
    foods = db.session.query(Food).all()

    food_json = list()

    for food in foods:
        food_dict = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein}
        food_json.append(food_dict)

    return jsonify(food_json)


@api.route("/foods/<int:id>")
def food_details_api():
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)

    res = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein}
    return jsonify(res)


@api.route("/workouts/")
def workouts_api():
    workouts = db.session.query(Workouts).all()

    workout_json = list()

    for workout in workouts:
        workout_dict = {'id': workout.id, 'name': workout.name, 'img': workout.img, 'category': workout.category, 'description': workout.description, 'met': workout.met, 'cid': workout.cid}
        workout_json.append(workout_dict)

    return jsonify(workout_json)


@api.route("/workouts/<int:id>")
def workouts_details_api():
    workout = db.session.query(Workouts).get(id)
    if workout is None:
        abort(404)

    res = {'id': workout.id, 'name': workout.name, 'img': workout.img, 'category': workout.category, 'description': workout.description, 'met': workout.met, 'cid': workout.cid}
    return jsonify(res)


@api.route("/stores/")
def stores_api():
    stores = db.session.query(Stores).all()

    stores_json = list()

    for store in stores:
        store_dict = {'id': store.id, 'gid': store.gid, 'name': store.name, 'location': store.location, 'price_level': store.price_level, 'ratings': store.ratings}
        stores_json.append(store_dict)

    return jsonify(stores_json)


@api.route("/stores/<int:id>")
def stores_details_api():
    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)

    res = {'id': store.id, 'gid': store.gid, 'name': store.name, 'location': store.location, 'price_level': store.price_level, 'ratings': store.ratings}
    return jsonify(res)


@api.route("/gyms/")
def gyms_api():
    gyms = db.session.query(Gyms).all()

    gyms_json = list()

    for gym in gyms:
        gym_dict = {'id': gym.id, 'gid': gym.gid, 'name': gym.name, 'location': gym.location, 'price_level': gym.price_level, 'ratings': gym.ratings}
        gyms_json.append(gym_dict)

    return jsonify(gyms_json)


@api.route("/gyms/<int:id>")
def gyms_details_api():
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)

    res = {'id': gym.id, 'gid': gym.gid, 'name': gym.name, 'location': gym.location, 'price_level': gym.price_level, 'ratings': gym.ratings}
    return jsonify(res)
