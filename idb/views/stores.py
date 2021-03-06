from flask import current_app as app
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import or_, func

from idb.models import Gyms, Images, Stores, Food
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords
from math import ceil

from .db_functions import gen_query

from backend.tools import unbinary, real_dist

from operator import attrgetter as at_get
from heapq import nsmallest
import base64

stores = Blueprint('stores', __name__)


@stores.route("/")
def overview():
    """
    The overview page for stores that shows all of the stores in the
    database.
    """

    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='name', type=str)
    order = request.args.get('order', default='asc', type=str)
    filters = request.args.get('filters', default='', type=str)

    attributes = [Stores.price_level]

    cat = db.session.query(Stores).distinct(attributes[0])
    f_crit = {c.price_level for c in cat}

    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)

    query = gen_query(Stores, items_per_page, page, sort, order, attributes, filters)
    total_count = gen_query(Stores, 10000000, 1, sort, order, attributes, filters).count()

    get_stores = query.all()
    items = [create_item(store) for store in get_stores]
    last_page = ceil(total_count / items_per_page)

    return render_template('stores/stores.html', items=items, sort=sort, order=order, filters=filters, current_page=page, last_page=last_page, f_crit=f_crit)


@stores.route("/<int:id>")
def detail(id):
    """
    The individual detail page for stores that show all of the information
    we have about a store item.
    """

    store = db.session.query(Stores).get(id)
    if store is None:
        abort(404)
    store.name = capwords(store.name)
    image = db.session.query(Images).get(store.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))

    # Search for the nearest gyms.
    gyms = db.session.query(Gyms).all()
    lat2 = at_get('lat')
    lng2 = at_get('lng')

    lat = lat2(store)
    lng = lng2(store)
    gym_list = nsmallest(4, gyms, lambda x: real_dist(lat, lng, lat2(x), lng2(x)))
    images = []
    for gym in gym_list:
        g_image = db.session.query(Images).get(gym.pic_id).pic
        images.append(unbinary(str(base64.b64encode(g_image))))
    # add some foods
    foods = db.session.query(Food).order_by(func.random()).limit(4).all()

    return render_template('stores/storesdetail.html', store=store, pic=img, gyms=gym_list, foods=foods, images=images, key=app.config['EMBED_API'])


def create_item(raw):
    """
    Create a dictionary item that represents the database item with
    some of the spurious things like internal ids and such for 
    presentation and organization on the actual site.  Also do any
    preprocessing like determing the URL for the detail page or processing
    images before being displayed.
    """

    image = db.session.query(Images).get(raw.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))

    # get a dict of all attributes and remove ones we don't care about
    item = vars(raw).copy()  # and don't alter the real thing
    item['name'] = capwords(item['name'])
    item['image'] = img
    item['detail_url'] = "stores/" + str(item['id'])
    item.pop('_sa_instance_state', None)
    item.pop('phone', None)
    item.pop('pic_id', None)
    item.pop('gid', None)
    item.pop('lat', None)
    item.pop('lng', None)

    return item
