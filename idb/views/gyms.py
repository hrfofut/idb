from flask import current_app as app
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Gyms, Images
# Later lets have a python thing that has all db calls
from idb import db

from backend.tools import unbinary
import base64

gyms = Blueprint('gyms', __name__)


@gyms.route("/")
def overview():
    # Really just show the first page, but don't use reroute() because
    # we want to keep the pretty URL
    return overview_page(1)


@gyms.route("/page/<int:page>")
def overview_page(page):
    items_per_page = app.config.get('ITEMS_PER_PAGE', 20)
    items = []
    get_gyms = db.session.query(Gyms).limit(items_per_page).offset((page - 1) * items_per_page).all()
    last_page = db.session.query(Gyms).count() / items_per_page
    for gym in get_gyms:
        image = db.session.query(Images).get(gym.pic_id).pic
        img = unbinary(str(base64.b64encode(image)))
        items.append([gym.name, img, gym.location, gym.ratings, gym.id])
    return render_template('gyms/gyms.html', items=items, current_page=page, last_page=last_page)


@gyms.route("/<int:id>")
def gyms_detail(id):
    gym = db.session.query(Gyms).get(id)
    if gym is None:
        abort(404)
    image = db.session.query(Images).get(gym.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))
    return render_template('gyms/gymsdetail.html', gym=gym, pic=img)
