from flask import Blueprint, render_template, abort, request
import requests
import json

from idb.models import Food, Workouts, Stores, Gyms, Images
from idb import db

from backend.tools import unbinary
import base64

general = Blueprint('general', __name__)


@general.route("/")
def splash(name=None):
    return render_template('index.html')


@general.route("/search", methods=['POST'])
def search():
    query = request.form['search']
    tokens = query.split(" ")
    food_items = []
    workout_items = []
    gym_items = []
    store_items = []

    for search in tokens:
        print("search: {}".format(search))
        get_foods = db.session.query(Food).filter(Food.name.like("%" + search + "%")).all()
        for val in get_foods:
            image = 'https://spoonacular.com/cdn/ingredients_500x500/' + val.img
            if ([val.name.title(), image, val.calorie, val.fat, val.id]) not in food_items:
                food_items.append([val.name.title(), image, val.calorie, val.fat, val.id])

        get_workouts = db.session.query(Workouts).filter(Workouts.name.like("%" + search + "%")).all()
        for val in get_workouts:
            if val.name != "" and ([val.name, val.img, val.category, val.muscle, val.id]) not in workout_items:
                workout_items.append([val.name, val.img, val.category, val.muscle, val.id])

        get_gyms = db.session.query(Gyms).filter(Gyms.name.like("%" + search + "%")).all()
        for gym in get_gyms:
            image = db.session.query(Images).get(gym.pic_id).pic
            img = unbinary(str(base64.b64encode(image)))
            if ([gym.name, img, gym.location, gym.ratings, gym.id]) not in gym_items:
                gym_items.append([gym.name, img, gym.location, gym.ratings, gym.id])

        get_stores = db.session.query(Stores).filter(Stores.name.like("%" + search + "%")).all()
        for store in get_stores:
            image = db.session.query(Images).get(store.pic_id).pic
            img = unbinary(str(base64.b64encode(image)))
            if ([store.name, img, store.location, store.ratings, store.id]) not in store_items:
                store_items.append([store.name, img, store.location, store.ratings, store.id])

    return render_template('search.html', search=query, food_items=food_items, workout_items=workout_items, gym_items=gym_items, store_items=store_items)


@general.route("/about")
def about():

    # get commits
    commit_count = {'total': 0, 'cindyqtruong': 0, 'BrandonHarrisonCode': 0, 'hrfofut': 0, 'straitlaced': 0, 'fantomats15': 0}
    req_commit = requests.get('https://api.github.com/repos/hrfofut/idb/stats/contributors')
    if req_commit.status_code == requests.codes.ok:
        req_commit_json = req_commit.json()
        if isinstance(req_commit_json, list):
            for cont in req_commit_json:
                commit_count[cont['author']['login']] = cont['total']
                commit_count['total'] += cont['total']

    # get issues
    logins = {'cindyqtruong': 0, 'BrandonHarrisonCode': 1, 'hrfofut': 2, 'straitlaced': 3, 'fantomats15': 4}
    iss_count = [0, 0, 0, 0, 0]
    iss_total = 0
    i = 1
    req_issues = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=' + str(i) + '&per_page=500')
    while (req_issues.status_code == requests.codes.ok) and (len(req_issues.json()) != 0):
        req_issues_json = req_issues.json()
        for issue in req_issues_json:
            iss_total += 1
            iss_count[logins[issue['user']['login']]] += 1
        i += 1
        req_issues = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=' + str(i) + '&per_page=500')
    iss_count.append(iss_total)
    return render_template('about.html', commits=commit_count, issues=iss_count)

# Error handling
