from flask import current_app as app
from flask import Blueprint, render_template, abort, request, redirect, url_for
import requests
import json

from idb.models import Food, Workouts, Stores, Gyms, Images
from idb import db

from backend.tools import unbinary
import base64

from math import ceil

from .foods import create_item as foods_create_item
from .workouts import create_item as workouts_create_item
from .gyms import create_item as gyms_create_item
from .stores import create_item as stores_create_item

from .db_functions import gen_query

general = Blueprint('general', __name__)


@general.route("/calc")
def calculator():
    """
    This page has a lot of information for calculating BMR and calorie info.
    """
    # abort(404)
    return render_template('test.html')


@general.route("/visualization")
def visualization():
    url = "http://api.musepy.me/"
    params = {"result_per_page": 99999}
    r_album = requests.get(url=url + "album", params=params).json()
    r_artist = requests.get(url=url + "artist", params=params).json()
    r_cities = requests.get(url=url + "city", params=params).json()
    r_songs = requests.get(url=url + "song", params=params).json()
    sizes = list()
    temp1 = dict()
    temp2 = dict()
    temp3 = dict()
    temp4 = dict()
    temp1['title'] = 'albums'
    temp1['Size'] = r_album['num_results']
    sizes.append(temp1)
    temp2['title'] = 'artists'
    temp2['Size'] = r_artist['num_results']
    sizes.append(temp2)
    temp3['title'] = 'cities'
    temp3['Size'] = r_cities['num_results']
    sizes.append(temp3)
    temp4['title'] = 'songs'
    temp4['Size'] = r_songs['num_results']
    sizes.append(temp4)
    data = {'chart_data': sizes}
    print(sizes)

    return render_template('visualization.html', ral=r_album, rar=r_artist, rc=r_cities, rs=r_songs, data=data)


@general.route("/")
def splash(name=None):
    return render_template('index.html')


@general.route("/search", methods=['POST', 'GET'])
def search():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    query = request.form.get('search', request.args.get('search'))

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)

    items = []
    foods = []
    workouts = []
    gyms = []
    stores = []
    # Goes through each of our models and searches them individually.
    tokens = query.split(" ")
    for search in tokens:
        food_query = gen_query(Food, items_per_page, page, sort, order, filter_string=search)
        food_count = gen_query(Food, 10000000, 1, 'name', order, filter_string=search).count()
        get_foods = food_query.all()
        for food in get_foods:
            food_item = foods_create_item(food)
            if food_item not in foods:
                foods.append(food_item)

        workouts_query = gen_query(Workouts, items_per_page, page, sort, order, filter_string=search)
        workouts_count = gen_query(Workouts, 10000000, 1, 'name', order, filter_string=search).count()
        get_workouts = workouts_query.all()
        for workout in get_workouts:
            workout_item = workouts_create_item(workout)
            if workout_item not in workouts:
                workouts.append(workout_item)

        gyms_query = gen_query(Gyms, items_per_page, page, sort, order, filter_string=search)
        gyms_count = gen_query(Gyms, 10000000, 1, 'name', order, filter_string=search).count()
        get_gyms = gyms_query.all()
        for gym in get_gyms:
            gym_item = gyms_create_item(gym)
            if gym_item not in gyms:
                gyms.append(gym_item)

        stores_query = gen_query(Stores, items_per_page, page, sort, order, filter_string=search)
        stores_count = gen_query(Stores, 10000000, 1, 'name', order, filter_string=search).count()
        get_stores = stores_query.all()
        for store in get_stores:
            store_item = stores_create_item(store)
            if store_item not in stores:
                stores.append(store_item)

    last_page = ceil(max(food_count, workouts_count, gyms_count, stores_count) / (items_per_page))

    # Next collect all the results
    items.append(foods)
    items.append(workouts)
    items.append(gyms)
    items.append(stores)

    for models in items:
        for item in models:
            t = item.get(sort, None)
            if t is not None:
                t = type(t)
                break

        if models:
            if t is str:
                models = sorted(models, key=lambda k: k.get(sort, ""))[::-1]
            else:
                models = sorted(models, key=lambda k: k.get(sort, 0))[::-1]

    attributes = {'name'}
    f_crit = set()  # filter criteria
    for models in items:
        for item in models:
            for key in item:
                attributes.add(key)
    return render_template('search.html', attributes=attributes, query=query, foods=foods, workouts=workouts, gyms=gyms, stores=stores, sort=sort, current_page=page, last_page=last_page)


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
            if issue['user']['login'] in logins:
                iss_total += 1
                iss_count[logins[issue['user']['login']]] += 1
        i += 1
        req_issues = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=' + str(i) + '&per_page=500')
    iss_count.append(iss_total)
    return render_template('about.html', commits=commit_count, issues=iss_count)
