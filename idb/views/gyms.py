from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from idb.models import Gyms, Images
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords
from math import ceil

from .db_functions import gen_query

from backend.tools import unbinary
import base64

gyms = Blueprint('gyms', __name__)


@gyms.route("/")
def overview():
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    filters = request.args.get('filters', default='', type=str)

    attribute = Gyms.price_level

    cat = db.session.query(Gyms).distinct(attribute)
    f_crit = set()  # filter criteria
    for c in cat:
        f_crit.add(c.price_level)

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []

    query = gen_query(Gyms, items_per_page, page, sort, order, attribute, filters)

    get_gyms = query.all()
    last_page = ceil(db.session.query(Gyms).count() / items_per_page)
    for gym in get_gyms:
        items.append(create_item(gym))
    return render_template('gyms/gyms.html', items=items, sort=sort, filters=filters, current_page=page, last_page=last_page, f_crit=f_crit)


@gyms.route("/<int:id>")
def detail(id):
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)
    image = db.session.query(Images).get(gym.pic_id).pic
    gym.name = capwords(gym.name)
    img = unbinary(str(base64.b64encode(image)))
    return render_template('gyms/gymsdetail.html', gym=gym, pic=img)


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
