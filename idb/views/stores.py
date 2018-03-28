from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images
# Later lets have a python thing that has all db calls
from idb import db

from backend.tools import unbinary
import base64

stores = Blueprint('stores', __name__)

first = 0
last = -1


@stores.route("/")
def stores_overview():
    items = []  # List of dicts that correspond to each store
    all_stores = db.session.query(Stores).all()
    for store in all_stores:
        image = db.session.query(Images).get(store.pic_id).pic
        img = unbinary(str(base64.b64encode(image)))
        items.append([store.name, img, store.location, store.ratings, store.id])
    return render_template('stores/stores.html', items=items)


@stores.route("/<int:id>")
def stores_detail(id):
    global last
    if last == -1:
        last = db.session.query(Stores).count()
        # ID 0 to store count returns certain store page, else return error
    if id < first or id > last:
        abort(404)
    store = db.session.query(Stores).get(id)
    image = db.session.query(Images).get(store.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))
    return render_template('stores/storesdetail.html', store=store, pic=img)
