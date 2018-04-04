from flask import current_app as app
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords

from backend.tools import unbinary
import base64

stores = Blueprint('stores', __name__)
asc = True


@stores.route("/", defaults={'page': 1, 'sort': 'name'})
@stores.route("/page/<int:page>")
@stores.route("/sort/<string:sort>", defaults={'page': 1})
@stores.route("/sort/<string:sort>/<int:page>")
def overview(page, sort):
    global asc
    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    if asc:
        get_stores = db.session.query(Stores).order_by(getattr(Stores, sort)).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = False
    else:
        get_stores = db.session.query(Stores).order_by(getattr(Stores, sort).desc()).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = True

    last_page = db.session.query(Stores).count() / items_per_page
    for store in get_stores:
        items.append(create_item(store))

    return render_template('stores/stores.html', items=items, sort=sort, current_page=page, last_page=last_page)


@stores.route("/<int:id>")
def detail(id):
    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)
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
    item.pop('_sa_instance_state', None)
    item.pop('phone', None)
    item.pop('pic_id', None)
    item.pop('gid', None)

    return item
