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


@general.route("/")
def splash(name=None):
    return render_template('index.html')


@general.route("/search", methods=['POST', 'GET'])
def search():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    query = request.form.get('search', request.args.get('search'))
    print(query)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []

    tokens = query.split(" ")
    for search in tokens:
        food_query = gen_query(Food, items_per_page, page, 'name', order, search)
        get_foods = food_query.all()
        for food in get_foods:
            items.append(foods_create_item(food))

        workouts_query = gen_query(Workouts, items_per_page, page, 'name', order, search)
        get_workouts = workouts_query.all()
        for workout in get_workouts:
            items.append(workouts_create_item(workout))

        gyms_query = gen_query(Gyms, items_per_page, page, 'name', order, search)
        get_gyms = gyms_query.all()
        for gym in get_gyms:
            items.append(gyms_create_item(gym))

        stores_query = gen_query(Stores, items_per_page, page, 'name', order, search)
        get_stores = stores_query.all()
        for store in get_stores:
            items.append(stores_create_item(store))

    last_page = ceil(len(items) / items_per_page)
    attributes = ['name']
    return render_template('search.html', attributes=attributes, query=query, items=items, sort=sort, current_page=page, last_page=last_page)


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
