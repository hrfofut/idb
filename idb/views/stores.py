from flask import current_app as app
from flask import Blueprint, render_template, abort, request, url_for
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords
from math import ceil
from .db_functions import gen_query

from backend.tools import unbinary
import base64

stores = Blueprint('stores', __name__)


@stores.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []

    query = gen_query(Stores, items_per_page, page, sort, order)
    get_stores = query.all()

    last_page = ceil(db.session.query(Stores).count() / items_per_page)
    for store in get_stores:
        items.append(create_item(store))

    return render_template('stores/stores.html', items=items, sort=sort, current_page=page, last_page=last_page)


@stores.route("/<int:id>")
def detail(id):
    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)
    store.name = capwords(store.name)
    image = db.session.query(Images).get(store.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))
    return render_template('stores/storesdetail.html', store=store, pic=img)


def create_item(raw):
    image = db.session.query(Images).get(raw.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))

    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = img
    item['detail_url'] = url_for('stores.detail', id=item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('phone', None)
    item.pop('pic_id', None)
    item.pop('gid', None)

    return item
