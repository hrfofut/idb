from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import or_, func

from idb.models import Gyms, Images, Stores, Workouts
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords
from math import ceil

from .db_functions import gen_query

from backend.tools import unbinary, real_dist

from operator import attrgetter as at_get
from heapq import nsmallest
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
    total_count = gen_query(Gyms, 10000000, 1, sort, order, attribute, filters).count()

    get_gyms = query.all()
    for gym in get_gyms:
        items.append(create_item(gym))
    last_page = ceil(total_count / items_per_page)

    return render_template('gyms/gyms.html', items=items, sort=sort, order=order, filters=filters, current_page=page, last_page=last_page, f_crit=f_crit)


@gyms.route("/<int:id>")
def detail(id):
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)
    image = db.session.query(Images).get(gym.pic_id).pic
    gym.name = capwords(gym.name)
    img = unbinary(str(base64.b64encode(image)))

    # Search for the nearest stores.
    stores = db.session.query(Stores).all()
    lat2 = at_get('lat')
    lng2 = at_get('lng')

    lat = lat2(gym)
    lng = lng2(gym)
    store_list = nsmallest(4, stores, lambda x: real_dist(lat, lng, lat2(x), lng2(x)))
    images = []
    for store in store_list:
        s_image = db.session.query(Images).get(store.pic_id).pic
        images.append(unbinary(str(base64.b64encode(s_image))))
    # add some workouts
    workouts = db.session.query(Workouts).filter(or_(Workouts.category == "conditioning exercise")).order_by(func.random()).limit(4).all()

    return render_template('gyms/gymsdetail.html', gym=gym, pic=img, stores=store_list, workouts=workouts, images=images, key=app.config['PLACE_API'])


def create_item(raw):
    image = db.session.query(Images).get(raw.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))

    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw)
    item['name'] = capwords(item['name'])
    item['image'] = img
    item['detail_url'] = "gyms/" + str(item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('phone', None)
    item.pop('pic_id', None)
    item.pop('gid', None)
    item.pop('lat', None)
    item.pop('lng', None)
    return item
