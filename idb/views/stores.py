from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images
# Later lets have a python thing that has all db calls
from idb import db
import base64
stores = Blueprint('stores', __name__)

first = 0
last = -1


@stores.route("/")
def stores_overview():
    img = 'https://www.colourbox.com/preview/19115718-supermarket-shop-vector-illustration.jpg'
    items = []
    # for val in stores_list:
    #     items.append([val['name'], val['img'], val['location'], val['ratings']])
    test = db.session.query(Stores).all()
    for val in test:
        image = db.session.query(Images).get(val.pic_id).pic
        x = str(base64.b64encode(image))
        x = x[2:]
        x = x[:-1]
        items.append([val.name, img, val.location, val.ratings, val.id, x])
    return render_template('stores/stores.html', items=items)


@stores.route("/<int:id>")
def stores_detail(id):
    global last
    # TODO: Have the template be filled from a database in the future
    if last == -1:
        last = db.session.query(Stores).count()
    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        abort(404)
    store = db.session.query(Stores).get(id)

    image = db.session.query(Images).get(store.pic_id).pic
    x = str(base64.b64encode(image))
    x = x[2:]
    x = x[:-1]
    return render_template('stores/storesdetail.html', store=store, pic=x)
