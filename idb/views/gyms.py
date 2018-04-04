from flask import current_app as app
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Gyms, Images
# Later lets have a python thing that has all db calls
from idb import db
from string import capwords

from backend.tools import unbinary
import base64

gyms = Blueprint('gyms', __name__)
asc = True


@gyms.route("/", defaults={'page': 1, 'sort': 'name'})
@gyms.route("/page/<int:page>")
@gyms.route("/sort/<string:sort>", defaults={'page': 1})
@gyms.route("/sort/<string:sort>/<int:page>")
def overview(page, sort):
    global asc
    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    if asc:
        get_gyms = db.session.query(Gyms).order_by(getattr(Gyms, sort)).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = False
    else:
        get_gyms = db.session.query(Gyms).order_by(getattr(Gyms, sort).desc()).limit(items_per_page).offset((page - 1) * items_per_page).all()
        asc = True

    last_page = db.session.query(Gyms).count() / items_per_page
    for gym in get_gyms:
        items.append(create_item(gym))
    return render_template('gyms/gyms.html', items=items, sort=sort, current_page=page, last_page=last_page)


@gyms.route("/<int:id>")
def detail(id):
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)
    image = db.session.query(Images).get(gym.pic_id).pic
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
