from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images
# Later lets have a python thing that has all db calls
from idb import db

from backend.tools import unbinary
import base64

stores = Blueprint('stores', __name__)


@stores.route("/")
def overview():
    # Really just show the first page, but don't use reroute() because
    # we want to keep the pretty URL
    return overview_page(1)


@stores.route("/page/<int:page>")
def overview_page(page):
    items_per_page = 20
    items = []
    get_stores = db.session.query(Stores).limit(items_per_page).offset((page - 1) * items_per_page).all()
    last_page = db.session.query(Stores).count() / items_per_page
    for store in get_stores:
        image = db.session.query(Images).get(store.pic_id).pic
        img = unbinary(str(base64.b64encode(image)))
        items.append([store.name, img, store.location, store.ratings, store.id])

    return render_template('stores/stores.html', items=items, current_page=page, last_page=last_page)


@stores.route("/<int:id>")
def stores_detail(id):
    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)
    image = db.session.query(Images).get(store.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))
    return render_template('stores/storesdetail.html', store=store, pic=img)
