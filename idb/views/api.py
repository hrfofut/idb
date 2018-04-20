from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from idb.models import Food, Workouts, Stores, Gyms
from idb import db

api = Blueprint('api', __name__)


@api.route("/")
def api_splash():
    return render_template('api.html')


@api.route("/foods/")
def food_api():
    """
    Returns all foods in DB
    """
    foods = db.session.query(Food).all()

    food_json = list()

    for food in foods:
        food_dict = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein, 'aisle': food.aisle, 'aisle2': food.aisle2, 'aisle3': food.aisle3}
        food_json.append(food_dict)

    return jsonify(food_json)


@api.route("/foods/<int:id>")
def food_details_api(id):
    """
    Returns a food from DB
    """
    food = db.session.query(Food).get(id)
    if food is None:
        abort(404)

    res = {'id': food.id, 'name': food.name, 'img': food.img, 'servings': food.servings, 'calorie': food.calorie, 'sodium': food.sodium, 'fat': food.fat, 'protein': food.protein, 'aisle': food.aisle, 'aisle2': food.aisle2, 'aisle3': food.aisle3}
    return jsonify(res)


@api.route("/workouts/")
def workouts_api():
    """
    Returns all workouts in DB
    """
    workouts = db.session.query(Workouts).all()

    workout_json = list()

    for workout in workouts:
        workout_dict = {'id': workout.id, 'name': workout.name, 'img': workout.img, 'category': workout.category, 'description': workout.description, 'met': workout.met, 'cid': workout.cid}
        workout_json.append(workout_dict)

    return jsonify(workout_json)


@api.route("/workouts/<int:id>")
def workouts_details_api(id):
    """
    Returns a workout from DB
    """
    workout = db.session.query(Workouts).get(id)
    if workout is None:
        abort(404)

    res = {'id': workout.id, 'name': workout.name, 'img': workout.img, 'category': workout.category, 'description': workout.description, 'met': workout.met, 'cid': workout.cid}
    return jsonify(res)


@api.route("/stores/")
def stores_api():
    """
    Returns all stores in DB
    """
    stores = db.session.query(Stores).all()

    stores_json = list()

    for store in stores:
        store_dict = {'id': store.id, 'gid': store.gid, 'name': store.name, 'location': store.location, 'price_level': store.price_level, 'ratings': store.ratings, 'latitude': store.lat, 'longitude': store.lng}
        stores_json.append(store_dict)

    return jsonify(stores_json)


@api.route("/stores/<int:id>")
def stores_details_api(id):
    """
    Returns a Store from DB
    """
    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)

    res = {'id': store.id, 'gid': store.gid, 'name': store.name, 'location': store.location, 'price_level': store.price_level, 'ratings': store.ratings, 'latitude': store.lat, 'longitude': store.lng}
    return jsonify(res)


@api.route("/gyms/")
def gyms_api():
    """
    Returns all gyms in DB
    """
    gyms = db.session.query(Gyms).all()

    gyms_json = list()

    for gym in gyms:
        gym_dict = {'id': gym.id, 'gid': gym.gid, 'name': gym.name, 'location': gym.location, 'price_level': gym.price_level, 'ratings': gym.ratings, 'latitude': gym.lat, 'longitude': gym.lng}
        gyms_json.append(gym_dict)

    return jsonify(gyms_json)


@api.route("/gyms/<int:id>")
def gyms_details_api(id):
    """
    Returns a gym from DB
    """
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)

    res = {'id': gym.id, 'gid': gym.gid, 'name': gym.name, 'location': gym.location, 'price_level': gym.price_level, 'ratings': gym.ratings, 'latitude': gym.lat, 'longitude': gym.lng}
    return jsonify(res)
